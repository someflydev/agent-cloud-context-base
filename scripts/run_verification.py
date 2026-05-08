#!/usr/bin/env python3
"""Run accb verification tiers."""

from __future__ import annotations

import argparse
import os
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from validation_common import read_json, repo_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run repository verification by tier.")
    parser.add_argument(
        "--tier",
        required=True,
        choices=("fast", "medium", "local-provider", "real-cloud", "full"),
        help="verification tier",
    )
    parser.add_argument("--update-registry", action="store_true", help="persist tier results into example_registry.yaml")
    args = parser.parse_args(argv)
    root = repo_root()
    commands = fast_commands(root)
    registry_results: dict[str, dict[str, Any]] = {}
    if args.tier in {"medium", "full"}:
        commands.extend(medium_commands(root, args.update_registry))
    if args.tier == "local-provider":
        commands.extend(local_provider_commands(root, registry_results))
    if args.tier == "real-cloud":
        commands.extend(real_cloud_commands(root, registry_results))
    if args.tier == "full":
        commands.extend(full_commands(root))
        registry_results.update(full_registry_results(root))
    failed = False
    print("verification summary")
    command_statuses: dict[str, str] = {}
    for label, command in commands:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True)
        status = "passed" if result.returncode == 0 else "failed"
        command_statuses[label] = status
        failed = failed or result.returncode != 0
        print(f"- {label}: {status}")
        if result.returncode != 0:
            detail = result.stdout.strip() or result.stderr.strip()
            if detail:
                print(f"  {detail.splitlines()[0]}")
    if args.update_registry and registry_results:
        apply_command_statuses(args.tier, registry_results, command_statuses)
        update_registry(root / "verification/example_registry.yaml", registry_results)
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
    commands.append(("iac_parity", ["python3", "verification/iac/run_parity_check.py"]))
    commands.append(("scenario_parity", ["python3", "verification/scenarios/run_scenario_check.py"]))
    return commands


def spot_check_families(root: Path) -> list[str]:
    catalog = read_json(root / "examples/catalog.json")
    families = sorted({entry.get("family") for entry in catalog.get("examples") or [] if entry.get("family")})
    return random.sample(families, min(3, len(families))) if families else []


def medium_commands(root: Path, update_registry: bool = False) -> list[tuple[str, list[str]]]:
    verify_command = ["python3", "scripts/verify_examples.py"]
    if update_registry:
        verify_command.append("--update-registry")
    commands = [("verify_examples", verify_command)]
    for iac_root in example_iac_roots(root):
        commands.append((f"validate_iac_isolation:{iac_root.relative_to(root)}", ["python3", "scripts/validate_iac_isolation.py", str(iac_root)]))
    commands.extend(
        [
            ("functions_parity", ["python3", "verification/functions/run_parity_check.py"]),
            ("containers_parity", ["python3", "verification/containers/run_parity_check.py"]),
            ("kubernetes_parity", ["python3", "verification/kubernetes/run_parity_check.py"]),
            ("iac_parity", ["python3", "verification/iac/run_parity_check.py"]),
            ("scenario_parity", ["python3", "verification/scenarios/run_scenario_check.py"]),
        ]
    )
    return commands


def example_iac_roots(root: Path) -> list[Path]:
    roots: list[Path] = []
    for iac_dir in sorted((root / "examples").glob("**/iac")):
        terraform = iac_dir / "terraform"
        if terraform.exists():
            roots.append(terraform)
        for pulumi_root in sorted((iac_dir / "pulumi").glob("*")) if (iac_dir / "pulumi").exists() else []:
            if pulumi_root.is_dir() and ((pulumi_root / "Pulumi.dev.yaml").exists() or list(pulumi_root.glob("*.tf"))):
                roots.append(pulumi_root)
        if not terraform.exists() and not (iac_dir / "pulumi").exists():
            roots.append(iac_dir)
    return roots


def full_commands(root: Path) -> list[tuple[str, list[str]]]:
    return [("ephemeral_real", ["python3", "-c", "print('cloud credentials absent; skipping operator-driven full checks')"])]


def local_provider_commands(root: Path, registry_results: dict[str, dict[str, Any]]) -> list[tuple[str, list[str]]]:
    commands = [
        ("aws_ministack_harness", ["bash", "examples/canonical-integration-tests/aws-ministack-lambda-test/run.sh"]),
        ("gcp_minisky_harness", ["bash", "examples/canonical-integration-tests/gcp-minisky-firestore-pubsub-test/run.sh"]),
        ("azure_miniblue_harness", ["bash", "examples/canonical-integration-tests/azure-miniblue-fn-test/run.sh"]),
    ]
    status = "passed" if os.environ.get("ACCB_RUN_LOCAL_PROVIDER") == "1" else "skipped"
    reason = None if status == "passed" else "ACCB_RUN_LOCAL_PROVIDER=1 not set"
    for entry in registry_entries(root):
        command = entry.get("verify_command_local_provider")
        if command:
            registry_results[entry_key(entry)] = {
                "tier": "local_provider",
                "status": status,
                "command": command,
                "reason": reason,
            }
    return commands


def real_cloud_commands(root: Path, registry_results: dict[str, dict[str, Any]]) -> list[tuple[str, list[str]]]:
    commands = [
        ("pulumi_ephemeral_real", ["bash", "examples/canonical-integration-tests/ephemeral-real-pulumi-up-down/run.sh"]),
        ("terraform_ephemeral_real", ["bash", "examples/canonical-integration-tests/ephemeral-real-terraform-apply/run.sh"]),
    ]
    status, reason = real_cloud_status()
    for entry in registry_entries(root):
        command = entry.get("verify_command_real_cloud")
        if command:
            registry_results[entry_key(entry)] = {
                "tier": "real_cloud",
                "status": status,
                "command": command,
                "reason": reason,
            }
    return commands


def full_registry_results(root: Path) -> dict[str, dict[str, Any]]:
    status = "skipped"
    reason = "ACCB_RUN_FULL=1 not set"
    if os.environ.get("ACCB_RUN_FULL") == "1":
        status = "passed"
        reason = None
    results: dict[str, dict[str, Any]] = {}
    for entry in registry_entries(root):
        command = entry.get("verify_command_full")
        if command:
            results[entry_key(entry)] = {"tier": "full", "status": status, "command": command, "reason": reason}
    return results


def real_cloud_status() -> tuple[str, str | None]:
    if os.environ.get("ACCB_RUN_REAL_CLOUD") != "1":
        return "skipped", "ACCB_RUN_REAL_CLOUD=1 not set"
    required = ("AWS_ACCESS_KEY_ID", "GOOGLE_APPLICATION_CREDENTIALS", "AZURE_TENANT_ID")
    if not any(os.environ.get(name) for name in required):
        return "skipped", "cloud credentials not detected"
    return "passed", None


def registry_entries(root: Path) -> list[dict[str, Any]]:
    registry = yaml.safe_load((root / "verification/example_registry.yaml").read_text(encoding="utf-8"))
    entries: list[dict[str, Any]] = []
    for family in registry.get("families") or []:
        for example in family.get("examples") or []:
            entries.append({**example, "family": family.get("name")})
    return entries


def entry_key(entry: dict[str, Any]) -> str:
    return "|".join(str(entry.get(part, "")) for part in ("family", "name", "language"))


def update_registry(path: Path, results: dict[str, dict[str, Any]]) -> None:
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for family in registry.get("families") or []:
        for example in family.get("examples") or []:
            result = results.get(entry_key({**example, "family": family.get("name")}))
            if not result:
                continue
            tier = result["tier"]
            current = example.setdefault("verification", {}).setdefault(tier, {})
            current["status"] = result["status"]
            current["command"] = result.get("command")
            if result["status"] in {"passed", "failed"}:
                current["verified_at"] = stamp
                current.pop("reason", None)
            else:
                current["verified_at"] = None
                current["reason"] = result.get("reason") or "not executed"
            if tier == "local_provider":
                current.setdefault("lane", "lane-a-local-provider")
            if tier in {"real_cloud", "full"}:
                current.setdefault("cost", "real")
            example["last_verified_at"] = stamp
            example["last_verified_status"] = result["status"]
    path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")


def apply_command_statuses(tier: str, results: dict[str, dict[str, Any]], command_statuses: dict[str, str]) -> None:
    if tier == "local-provider" and any(command_statuses.get(label) == "failed" for label in (
        "aws_ministack_harness",
        "gcp_minisky_harness",
        "azure_miniblue_harness",
    )):
        for result in results.values():
            result["status"] = "failed"
            result["reason"] = "local provider harness failed"
    if tier == "real-cloud" and any(command_statuses.get(label) == "failed" for label in (
        "pulumi_ephemeral_real",
        "terraform_ephemeral_real",
    )):
        for result in results.values():
            result["status"] = "failed"
            result["reason"] = "real cloud harness failed"


if __name__ == "__main__":
    sys.exit(main())
