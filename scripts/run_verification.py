#!/usr/bin/env python3
"""Run accb verification tiers."""

from __future__ import annotations

import argparse
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

from validation_common import read_json, repo_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run repository verification by tier.")
    parser.add_argument("--tier", required=True, choices=("fast", "medium", "full"), help="verification tier")
    args = parser.parse_args(argv)
    root = repo_root()
    commands = fast_commands(root)
    if args.tier in {"medium", "full"}:
        commands.extend(medium_commands(root))
    if args.tier == "full":
        commands.extend(full_commands(root))
    failed = False
    print("verification summary")
    for label, command in commands:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True)
        status = "passed" if result.returncode == 0 else "failed"
        failed = failed or result.returncode != 0
        print(f"- {label}: {status}")
        if result.returncode != 0:
            detail = result.stdout.strip() or result.stderr.strip()
            if detail:
                print(f"  {detail.splitlines()[0]}")
    print(f"overall: {'failed' if failed else 'passed'}")
    return 1 if failed else 0


def fast_commands(root: Path) -> list[tuple[str, list[str]]]:
    commands = [
        ("validate_context", ["python3", "scripts/validate_context.py"]),
        ("validate_manifests", ["python3", "scripts/validate_manifests.py"]),
    ]
    for family in spot_check_families(root):
        commands.append((f"verify_examples:{family}", ["python3", "scripts/verify_examples.py", "--family", family]))
    commands.append(
        (
            "accb_payload_snapshot",
            [
                "python3",
                "scripts/accb_payload.py",
                "--archetype",
                "cloud-function-repo",
                "--primary-stack",
                "aws-lambda-python",
                "--primary-language",
                "python",
                "--provider",
                "aws",
                "--runtime-tier",
                "function",
                "--iac-tool",
                "pulumi-python",
                "--manifest",
                "func-aws-lambda-python",
                "--output-dir",
                "/tmp/accb-payload-fast",
            ],
        )
    )
    return commands


def spot_check_families(root: Path) -> list[str]:
    catalog = read_json(root / "examples/catalog.json")
    families = sorted({entry.get("family") for entry in catalog.get("examples") or [] if entry.get("family")})
    return random.sample(families, min(3, len(families))) if families else []


def medium_commands(root: Path) -> list[tuple[str, list[str]]]:
    commands = [("verify_examples", ["python3", "scripts/verify_examples.py"])]
    for iac_root in example_iac_roots(root):
        commands.append((f"validate_iac_isolation:{iac_root.relative_to(root)}", ["python3", "scripts/validate_iac_isolation.py", str(iac_root)]))
    return commands


def example_iac_roots(root: Path) -> list[Path]:
    roots: list[Path] = []
    for iac_dir in sorted((root / "examples").glob("**/iac")):
        terraform = iac_dir / "terraform"
        if terraform.exists():
            roots.append(terraform)
        for pulumi_root in sorted((iac_dir / "pulumi").glob("*")) if (iac_dir / "pulumi").exists() else []:
            if pulumi_root.is_dir():
                roots.append(pulumi_root)
        if not terraform.exists() and not (iac_dir / "pulumi").exists():
            roots.append(iac_dir)
    return roots


def full_commands(root: Path) -> list[tuple[str, list[str]]]:
    return [("ephemeral_real", ["python3", "-c", "print('cloud credentials absent; skipping operator-driven full checks')"])]


if __name__ == "__main__":
    sys.exit(main())
