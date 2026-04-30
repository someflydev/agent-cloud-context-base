#!/usr/bin/env python3
"""Verify generated repo-local `.accb/` payload integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_MISMATCH = 1
EXIT_ENV = 2


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def verify(repo: Path, run_commands: bool = True) -> tuple[int, dict[str, Any]]:
    accb = repo / ".accb"
    index = load_json(accb / "INDEX.json")
    selection = load_json(accb / "profile/selection.json")
    matrix = load_json(accb / "validation/MATRIX.json")
    scenarios = load_json(accb / "profile/scenario-patterns.json")

    mismatches: list[dict[str, str]] = []
    for item in index.get("files", []):
        rel = item["path"]
        path = repo / rel
        if not path.exists():
            mismatches.append({"path": rel, "reason": "missing"})
        elif sha256_path(path) != item["sha256"]:
            mismatches.append({"path": rel, "reason": "hash-mismatch"})

    doctrine_refs: list[str] = []
    for candidate in (repo / "AGENT.md", repo / "CLAUDE.md", accb / "SESSION_BOOT.md", accb / "specs/AGENT_RULES.md"):
        if candidate.exists():
            doctrine_refs.append(candidate.read_text(encoding="utf-8", errors="replace"))
    missing_doctrines = [
        doctrine for doctrine in selection.get("doctrines", []) if not any(doctrine in text for text in doctrine_refs)
    ]

    scenario_missing = [
        pattern
        for pattern in selection.get("scenario_patterns", [])
        if pattern not in scenarios.get("patterns", {})
    ]

    signal_mismatches: list[str] = []
    iac_tool = selection.get("iac_tool")
    if iac_tool == "terraform" and not (repo / "iac/terraform/dev").exists():
        signal_mismatches.append("missing iac/terraform/dev for terraform profile")
    if isinstance(iac_tool, str) and iac_tool.startswith("pulumi-"):
        language = iac_tool.removeprefix("pulumi-")
        if not (repo / "iac/pulumi" / language / "Pulumi.yaml").exists():
            signal_mismatches.append(f"missing iac/pulumi/{language}/Pulumi.yaml for {iac_tool} profile")

    command_results: list[dict[str, Any]] = []
    if run_commands:
        for gate in matrix.get("gates", {}).values():
            command = gate.get("command")
            if not command or "<" in command or ">" in command or gate.get("deferred"):
                continue
            result = subprocess.run(command, cwd=repo, shell=True, text=True, capture_output=True)
            command_results.append({"id": gate["id"], "command": command, "returncode": result.returncode})

    failed_commands = [row for row in command_results if row["returncode"] != 0]
    report = {
        "repo": repo.as_posix(),
        "payload_mismatches": mismatches,
        "missing_doctrine_references": missing_doctrines,
        "missing_scenario_patterns": scenario_missing,
        "repo_signal_mismatches": signal_mismatches,
        "command_results": command_results,
    }
    dirty = bool(mismatches or missing_doctrines or scenario_missing or signal_mismatches or failed_commands)
    return (EXIT_MISMATCH if dirty else EXIT_OK), report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify the `.accb/` payload in a generated repo.")
    parser.add_argument("--repo", default=".", help="Repo root containing `.accb/`.")
    parser.add_argument("--fix", action="store_true", help="Rebuild `.accb/` from saved selection.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo = Path(args.repo).resolve()
    try:
        if args.fix:
            from accb_payload import build_payload

            selection = load_json(repo / ".accb/profile/selection.json")
            build_payload(
                archetype=selection["archetype"],
                primary_stack=selection["primary_stack"],
                primary_language=selection["primary_language"],
                provider=selection["provider"],
                runtime_tier=selection["runtime_tier"],
                iac_tool=selection["iac_tool"],
                manifest=selection["manifest"],
                support_services=selection.get("support_services", []),
                scenario_patterns=selection.get("scenario_patterns", []),
                target_root=repo,
                include_startup_features=bool(selection.get("startup_features", {}).get("budget_report_enabled")),
            )
        code, report = verify(repo)
    except FileNotFoundError as exc:
        print(f"missing .accb payload file: {exc.filename}", file=sys.stderr)
        return EXIT_ENV
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ENV
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("accb verify")
        print(f"- repo: {report['repo']}")
        print(f"- payload mismatches: {len(report['payload_mismatches']) or 'none'}")
        print(f"- missing doctrine references: {', '.join(report['missing_doctrine_references']) or 'none'}")
        print(f"- missing scenario patterns: {', '.join(report['missing_scenario_patterns']) or 'none'}")
        print(f"- repo signal mismatches: {', '.join(report['repo_signal_mismatches']) or 'none'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
