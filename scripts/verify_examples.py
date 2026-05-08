#!/usr/bin/env python3
"""Verify registered examples and optionally update verification timestamps."""

from __future__ import annotations

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from validation_common import read_json, read_yaml, repo_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify canonical examples declared in the registry.")
    parser.add_argument("--family", help="only verify one family")
    parser.add_argument(
        "--tier",
        choices=("smoke", "local-provider", "real-cloud", "full"),
        default="smoke",
        help=(
            "verification tier: smoke runs default smoke + IaC isolation; "
            "local-provider adds Lane A commands when registered; real-cloud "
            "adds Lane B commands when registered; full adds all registered gates"
        ),
    )
    parser.add_argument("--update-registry", action="store_true", help="write last verification status into registry")
    parser.add_argument("--parallel", type=int, default=1, help="number of examples to verify concurrently")
    args = parser.parse_args(argv)
    root = repo_root()
    registry_path = root / "verification/example_registry.yaml"
    registry = read_yaml(registry_path)
    catalog = read_json(root / "examples/catalog.json")
    entries = collect_examples(registry, catalog, args.family)
    if not entries:
        print("no examples registered")
        return 0
    workers = max(1, args.parallel)
    if workers == 1:
        results = [verify_one(root, entry, args.tier) for entry in entries]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(lambda entry: verify_one(root, entry, args.tier), entries))
    failed = [result for result in results if not result["ok"]]
    for result in results:
        status = "passed" if result["ok"] else "failed"
        print(f"{result['id']}: {status} ({result['message']})")
    if args.update_registry:
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        update_registry(registry, results, stamp)
        registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
    return 1 if failed else 0


def collect_examples(registry: dict[str, Any], catalog: dict[str, Any], family: str | None) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(registry, list):
        registry_entries = registry
    else:
        registry_entries = registry.get("examples") or registry.get("entries") or []
        for fam in registry.get("families") or []:
            if family and fam.get("name") != family:
                continue
            for example in fam.get("examples") or []:
                registry_entries.append({**example, "family": fam.get("name")})
    for example in registry_entries:
        if not isinstance(example, dict):
            continue
        if family and example.get("family") != family:
            continue
        entries.append(example)
    catalog_examples = catalog.get("examples") or []
    if family:
        catalog_examples = [entry for entry in catalog_examples if entry.get("family") == family]
    for example in catalog_examples:
        if not any(example_key(item) == example_key(example) for item in entries):
            entries.append(example)
    return entries


def example_key(entry: dict[str, Any]) -> str:
    if entry.get("family") and entry.get("name") and entry.get("language"):
        return "|".join(str(entry.get(part, "")) for part in ("family", "name", "language"))
    return str(entry.get("id") or entry.get("path") or entry.get("name") or "")


def verify_one(root: Path, entry: dict[str, Any], tier: str) -> dict[str, Any]:
    example_id = example_key(entry)
    for file_name in entry.get("files") or []:
        if not (root / file_name).exists():
            return {"id": example_id, "ok": False, "message": f"missing file {file_name}", "tiers": {}}
    commands = tier_commands(entry, tier)
    if not commands:
        return {"id": example_id, "ok": True, "message": "no verify_command declared", "tiers": {}}
    messages: list[str] = []
    tier_results: dict[str, dict[str, Any]] = {}
    ok = True
    for label, command, required in commands:
        if not command:
            if required:
                tier_results[label] = {"status": "failed", "command": None, "reason": "missing required command"}
                return {
                    "id": example_id,
                    "ok": False,
                    "message": f"missing required {label} command",
                    "tiers": tier_results,
                }
            tier_results[label] = {"status": "skipped", "command": None, "reason": "command not declared"}
            messages.append(f"{label}: skipped")
            continue
        skip_reason = gated_skip_reason(label)
        if skip_reason:
            tier_results[label] = {"status": "skipped", "command": command, "reason": skip_reason}
            messages.append(f"{label}: skipped ({skip_reason})")
            continue
        result = subprocess.run(command, cwd=root, shell=True, text=True, capture_output=True, timeout=300)
        message = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part) or f"exit {result.returncode}"
        messages.append(f"{label}: {message[:160]}")
        if result.returncode != 0 and sandbox_skip_reason(message):
            tier_results[label] = {"status": "skipped", "command": command, "reason": sandbox_skip_reason(message)}
            messages[-1] = f"{label}: skipped ({sandbox_skip_reason(message)})"
            continue
        tier_results[label] = {"status": "passed" if result.returncode == 0 else "failed", "command": command}
        if result.returncode != 0:
            ok = False
            break
    return {"id": example_id, "ok": ok, "message": "; ".join(messages)[:200], "tiers": tier_results}


def tier_commands(entry: dict[str, Any], tier: str) -> list[tuple[str, str | None, bool]]:
    smoke = entry.get("verify_command")
    local_provider = entry.get("verify_command_local_provider")
    real_cloud = entry.get("verify_command_real_cloud")
    full = entry.get("verify_command_full")
    if tier == "smoke":
        return [("smoke", smoke, False)]
    if tier == "local-provider":
        return [("smoke", smoke, False), ("local-provider", local_provider, False)]
    if tier == "real-cloud":
        return [("smoke", smoke, False), ("real-cloud", real_cloud, False)]
    return [
        ("smoke", smoke, False),
        ("local-provider", local_provider, False),
        ("real-cloud", real_cloud, False),
        ("full", full, False),
    ]


def gated_skip_reason(label: str) -> str | None:
    import os

    if label == "local-provider" and os.environ.get("ACCB_RUN_LOCAL_PROVIDER") != "1":
        return "ACCB_RUN_LOCAL_PROVIDER=1 not set"
    if label == "real-cloud":
        if os.environ.get("ACCB_RUN_REAL_CLOUD") != "1":
            return "ACCB_RUN_REAL_CLOUD=1 not set"
        required = ("AWS_ACCESS_KEY_ID", "GOOGLE_APPLICATION_CREDENTIALS", "AZURE_TENANT_ID")
        if not any(os.environ.get(name) for name in required):
            return "cloud credentials not detected"
    if label == "full":
        if os.environ.get("ACCB_RUN_FULL") != "1":
            return "ACCB_RUN_FULL=1 not set"
    return None


def sandbox_skip_reason(message: str) -> str | None:
    lowered = message.lower()
    if "docker daemon socket" in lowered and ("permission denied" in lowered or "operation not permitted" in lowered):
        return "docker daemon unavailable in current environment"
    return None


def update_registry(registry: dict[str, Any], results: list[dict[str, Any]], stamp: str) -> None:
    by_id = {result["id"]: result for result in results}
    for fam in registry.get("families") or []:
        for example in fam.get("examples") or []:
            example_id = example_key({**example, "family": fam.get("name")})
            result = by_id.get(example_id)
            if result:
                verification = example.setdefault("verification", {})
                for tier, tier_result in (result.get("tiers") or {}).items():
                    key = tier.replace("-", "_")
                    current = verification.setdefault(key, {})
                    current["status"] = tier_result["status"]
                    current["command"] = tier_result.get("command")
                    if tier_result["status"] in {"passed", "failed"}:
                        current["verified_at"] = stamp
                        current.pop("reason", None)
                    else:
                        current["verified_at"] = None
                        current["reason"] = tier_result.get("reason") or "not executed"
                example["last_verified_at"] = stamp
                example["last_verified_status"] = "passed" if result["ok"] else "failed"


if __name__ == "__main__":
    sys.exit(main())
