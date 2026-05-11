#!/usr/bin/env python3
"""Run accb verification tiers."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from validation_common import read_json, repo_root


FAST_FAMILY_COVERAGE = (
    "canonical-aws-lambda",
    "canonical-gcp-functions",
    "canonical-azure-functions",
    "canonical-cloud-run",
    "canonical-iac-pulumi",
)


@dataclass(frozen=True)
class CommandSpec:
    label: str
    command: list[str] | str
    registry_key: str | None = None
    tier: str | None = None
    skipped_reason: str | None = None
    shell: bool = False


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
    if args.tier in {"medium", "full"}:
        commands.extend(medium_commands(root, args.update_registry))
    if args.tier == "local-provider":
        commands.extend(local_provider_commands(root))
    if args.tier == "real-cloud":
        commands.extend(real_cloud_commands(root))
    if args.tier == "full":
        commands.extend(full_commands(root))
        commands.extend(full_registry_commands(root))
    failed = False
    print("verification summary")
    command_statuses: dict[str, str] = {}
    registry_results: dict[str, dict[str, Any]] = {}
    for spec in commands:
        result = run_spec(spec, root)
        status, reason = command_result_status(result, spec.skipped_reason)
        command_statuses[spec.label] = status
        failed = failed or status == "failed"
        print(f"- {spec.label}: {status}")
        detail = reason or first_detail(result)
        if detail and status in {"failed", "skipped"}:
            print(f"  {detail}")
        if spec.registry_key and spec.tier:
            registry_results[spec.registry_key] = {
                "tier": spec.tier,
                "status": status,
                "command": command_text(spec.command),
                "reason": reason,
            }
    if args.update_registry and registry_results:
        update_registry(root / "verification/example_registry.yaml", registry_results)
    print(f"overall: {'failed' if failed else 'passed'}")
    return 1 if failed else 0


def fast_commands(root: Path) -> list[CommandSpec]:
    commands = [
        CommandSpec("validate_context", ["python3", "scripts/validate_context.py"]),
        CommandSpec("validate_manifests", ["python3", "scripts/validate_manifests.py"]),
    ]
    for family in deterministic_fast_families(root):
        commands.append(CommandSpec(f"verify_examples:{family}", ["python3", "scripts/verify_examples.py", "--family", family]))
    commands.append(
        CommandSpec(
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
    commands.extend(
        [
            CommandSpec("functions_parity", ["python3", "verification/functions/run_parity_check.py"]),
            CommandSpec("containers_parity", ["python3", "verification/containers/run_parity_check.py"]),
            CommandSpec("kubernetes_parity", ["python3", "verification/kubernetes/run_parity_check.py"]),
            CommandSpec("iac_parity", ["python3", "verification/iac/run_parity_check.py"]),
            CommandSpec("scenario_parity", ["python3", "verification/scenarios/run_scenario_check.py"]),
        ]
    )
    return commands


def deterministic_fast_families(root: Path) -> list[str]:
    catalog = read_json(root / "examples/catalog.json")
    families = sorted({entry.get("family") for entry in catalog.get("examples") or [] if entry.get("family")})
    selected = [family for family in FAST_FAMILY_COVERAGE if family in families]
    return selected or families[:3]


def medium_commands(root: Path, update_registry: bool = False) -> list[CommandSpec]:
    verify_command = ["python3", "scripts/verify_examples.py"]
    if update_registry:
        verify_command.append("--update-registry")
    commands = [CommandSpec("verify_examples", verify_command)]
    for iac_root in example_iac_roots(root):
        commands.append(CommandSpec(f"validate_iac_isolation:{iac_root.relative_to(root)}", ["python3", "scripts/validate_iac_isolation.py", str(iac_root)]))
    commands.extend(
        [
            CommandSpec("functions_parity", ["python3", "verification/functions/run_parity_check.py"]),
            CommandSpec("containers_parity", ["python3", "verification/containers/run_parity_check.py"]),
            CommandSpec("kubernetes_parity", ["python3", "verification/kubernetes/run_parity_check.py"]),
            CommandSpec("iac_parity", ["python3", "verification/iac/run_parity_check.py"]),
            CommandSpec("scenario_parity", ["python3", "verification/scenarios/run_scenario_check.py"]),
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


def full_commands(root: Path) -> list[CommandSpec]:
    return [CommandSpec("full_gate", ["python3", "-c", "print('skipped: no full verification commands are declared')"])]


def local_provider_commands(root: Path) -> list[CommandSpec]:
    if os.environ.get("ACCB_RUN_LOCAL_PROVIDER") != "1":
        reason = "ACCB_RUN_LOCAL_PROVIDER=1 not set"
        return [
                CommandSpec(
                    f"local_provider:{entry['family']}:{entry['name']}:{entry['language']}",
                    entry["verify_command_local_provider"],
                    registry_key=entry_key(entry),
                    tier="local_provider",
                    skipped_reason=reason,
                    shell=True,
                )
            for entry in registry_entries(root)
            if entry.get("verify_command_local_provider")
        ]
    commands: list[CommandSpec] = []
    for entry in registry_entries(root):
        command = entry.get("verify_command_local_provider")
        if command:
            commands.append(
                CommandSpec(
                    f"local_provider:{entry['family']}:{entry['name']}:{entry['language']}",
                    command,
                    registry_key=entry_key(entry),
                    tier="local_provider",
                    shell=True,
                )
            )
    return commands


def real_cloud_commands(root: Path) -> list[CommandSpec]:
    commands: list[CommandSpec] = []
    for entry in registry_entries(root):
        command = entry.get("verify_command_real_cloud")
        if command:
            reason = real_cloud_skip_reason(entry)
            commands.append(
                CommandSpec(
                    f"real_cloud:{entry['family']}:{entry['name']}:{entry['language']}",
                    command,
                    registry_key=entry_key(entry),
                    tier="real_cloud",
                    skipped_reason=reason,
                    shell=reason is None,
                )
            )
    return commands


def full_registry_commands(root: Path) -> list[CommandSpec]:
    commands: list[CommandSpec] = []
    for entry in registry_entries(root):
        command = entry.get("verify_command_full")
        if command:
            reason = None if os.environ.get("ACCB_RUN_FULL") == "1" else "ACCB_RUN_FULL=1 not set"
            commands.append(
                CommandSpec(
                    f"full:{entry['family']}:{entry['name']}:{entry['language']}",
                    command,
                    registry_key=entry_key(entry),
                    tier="full",
                    skipped_reason=reason,
                    shell=reason is None,
                )
            )
    return commands


def real_cloud_skip_reason(entry: dict[str, Any]) -> str | None:
    if os.environ.get("ACCB_RUN_REAL_CLOUD") != "1":
        return "ACCB_RUN_REAL_CLOUD=1 not set"
    provider = entry.get("provider")
    required_by_provider = {
        "aws": ("AWS_ACCESS_KEY_ID",),
        "gcp": ("GOOGLE_APPLICATION_CREDENTIALS",),
        "azure": ("AZURE_TENANT_ID",),
    }
    required = required_by_provider.get(str(provider), ())
    if required and not all(os.environ.get(name) for name in required):
        return f"{provider} cloud credentials not detected"
    return None


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
            refresh_derived_status(example)
    path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")


def run_spec(spec: CommandSpec, root: Path) -> subprocess.CompletedProcess[str]:
    if spec.skipped_reason:
        return subprocess.CompletedProcess(spec.command, 0, stdout=f"skipped: {spec.skipped_reason}\n", stderr="")
    return subprocess.run(spec.command, cwd=root, text=True, capture_output=True, shell=spec.shell)


def command_result_status(result: subprocess.CompletedProcess[str], skipped_reason: str | None = None) -> tuple[str, str | None]:
    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    skip_line = next((line.strip() for line in output.splitlines() if line.strip().startswith("skipped:")), None)
    if skip_line:
        return "skipped", skip_line.removeprefix("skipped:").strip() or skipped_reason
    if skipped_reason:
        return "skipped", skipped_reason
    if result.returncode == 0:
        return "passed", None
    return "failed", first_detail(result) or f"exit code {result.returncode}"


def first_detail(result: subprocess.CompletedProcess[str]) -> str | None:
    detail = result.stdout.strip() or result.stderr.strip()
    return detail.splitlines()[0] if detail else None


def command_text(command: list[str] | str) -> str:
    return command if isinstance(command, str) else " ".join(command)


def refresh_derived_status(example: dict[str, Any]) -> None:
    verification = example.get("verification") or {}
    passed = [
        tier
        for tier, result in verification.items()
        if isinstance(result, dict) and result.get("status") == "passed" and result.get("verified_at")
    ]
    if passed:
        latest = max((verification[tier]["verified_at"], tier) for tier in passed)
        example["last_verified_at"] = latest[0]
        example["last_verified_status"] = "passed"
        return
    failed = [
        tier
        for tier, result in verification.items()
        if isinstance(result, dict) and result.get("status") == "failed" and result.get("verified_at")
    ]
    if failed:
        latest = max((verification[tier]["verified_at"], tier) for tier in failed)
        example["last_verified_at"] = latest[0]
        example["last_verified_status"] = "failed"
        return
    skipped = [
        tier
        for tier, result in verification.items()
        if isinstance(result, dict) and result.get("status") == "skipped"
    ]
    if skipped:
        example["last_verified_at"] = None
        example["last_verified_status"] = "skipped"


if __name__ == "__main__":
    sys.exit(main())
