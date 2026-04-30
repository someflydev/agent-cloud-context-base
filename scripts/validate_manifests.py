#!/usr/bin/env python3
"""Validate accb manifest schema and cross references."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from validation_common import path_exists_or_planned, read_json, read_yaml, repo_root, rel


REQUIRED_FIELDS = {
    "schema_version",
    "name",
    "description",
    "archetype",
    "primary_stack",
    "secondary_stacks",
    "provider",
    "runtime_tier",
    "primary_language",
    "generated_repo_target",
    "iac_tool",
    "triggers",
    "aliases",
    "scenario_patterns",
    "required_context",
    "optional_context",
    "preferred_examples",
    "recommended_templates",
    "repo_signals",
    "task_hints",
    "warnings",
    "bootstrap_defaults",
    "iac_layout",
    "env_isolation",
    "cloud_integration_test_strategy",
    "cost_band_per_test_run",
    "smoke_test_expectations",
    "prompt_first_support",
}
PROVIDERS = {"aws", "gcp", "azure", "multi"}
RUNTIME_TIERS = {"function", "managed_container", "k8s", None}
IAC_TOOLS = {"terraform", "pulumi-python", "pulumi-typescript", "pulumi-go", "pulumi-dotnet"}
TEST_STRATEGIES = {"localstack", "emulator", "azurite", "ephemeral_real", "record_replay"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate manifest schema and cross references.")
    parser.add_argument("manifest_name", nargs="?", help="optional manifest name or path")
    args = parser.parse_args(argv)
    root = repo_root()
    paths = select_paths(root, args.manifest_name)
    if not paths:
        print("no manifest files found", file=sys.stderr)
        return 1
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    for path in paths:
        validate_one(root, path, errors, warnings, notes)
    if errors:
        print("manifest validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARN: {warning}")
        for note in notes:
            print(f"NOTE: {note}")
        return 1
    print(f"manifest validation passed ({len(paths)} file(s))")
    for warning in warnings:
        print(f"WARN: {warning}")
    for note in notes:
        print(f"NOTE: {note}")
    return 0


def select_paths(root: Path, name: str | None) -> list[Path]:
    if not name:
        return sorted((root / "manifests").glob("*.yaml"))
    candidate = Path(name)
    if candidate.suffix:
        return [candidate if candidate.is_absolute() else root / candidate]
    return [root / "manifests" / f"{name}.yaml"]


def validate_one(root: Path, path: Path, errors: list[str], warnings: list[str], notes: list[str]) -> None:
    if not path.exists():
        errors.append(f"manifest missing: {rel(path, root)}")
        return
    data = read_yaml(path)
    if not isinstance(data, dict):
        errors.append(f"{rel(path, root)} must be a mapping")
        return
    name = data.get("name")
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        errors.append(f"{rel(path, root)} missing fields {missing}")
    if data.get("schema_version") != 2:
        errors.append(f"{rel(path, root)} schema_version must be 2")
    if name != path.stem:
        errors.append(f"{rel(path, root)} name must match file stem")

    profile = read_json(root / "context/accb/profile-rules.json")
    scenario_map = read_yaml(root / "context/scenarios/scenario-profile-map.yaml")
    manifests = set((profile.get("manifest_capabilities") or {}).keys())
    archetypes = {p.stem for p in (root / "context/archetypes").glob("*.md")}
    stacks = {p.stem for p in (root / "context/stacks").glob("*.md")}
    workflows = {p.stem for p in (root / "context/workflows").glob("*.md")}
    patterns = scenario_map.get("patterns") or {}

    if name not in manifests:
        errors.append(f"{rel(path, root)} name not registered in profile-rules manifest_capabilities")
    if data.get("archetype") not in archetypes:
        errors.append(f"{rel(path, root)} archetype does not resolve")
    generated = data.get("generated_repo_target")
    if not isinstance(generated, bool):
        errors.append(f"{rel(path, root)} generated_repo_target must be boolean")
    provider = data.get("provider")
    if provider not in PROVIDERS:
        errors.append(f"{rel(path, root)} provider must be one of {sorted(PROVIDERS)}")
    if provider == "multi" and generated is not False:
        errors.append(f"{rel(path, root)} provider multi is only valid for catalog-only manifests")
    runtime_tier = data.get("runtime_tier")
    if runtime_tier not in RUNTIME_TIERS:
        errors.append(f"{rel(path, root)} runtime_tier is invalid: {runtime_tier!r}")
    if data.get("iac_tool") not in IAC_TOOLS:
        errors.append(f"{rel(path, root)} iac_tool is invalid: {data.get('iac_tool')!r}")
    primary_stack = data.get("primary_stack")
    if generated is True and primary_stack not in stacks:
        errors.append(f"{rel(path, root)} generated manifest primary_stack does not resolve")
    if generated is False:
        if primary_stack == "none":
            notes.append(f"{rel(path, root)} is catalog-only in v1, not a new_cloud_repo.py target")
        elif primary_stack not in stacks:
            errors.append(f"{rel(path, root)} primary_stack does not resolve")
    if generated is True and (runtime_tier is None or provider == "multi" or primary_stack == "none"):
        errors.append(f"{rel(path, root)} generated manifest uses reference-only values")

    for stack in data.get("secondary_stacks") or []:
        if stack not in stacks:
            errors.append(f"{rel(path, root)} secondary stack does not resolve: {stack}")
    for key in ("required_context", "optional_context", "preferred_examples", "recommended_templates"):
        for entry in data.get(key) or []:
            if not path_exists_or_planned(root, entry):
                warnings.append(f"{rel(path, root)} {key} entry is planned or missing: {entry}")
    for task in data.get("task_hints") or []:
        if task not in workflows:
            errors.append(f"{rel(path, root)} task_hints entry does not resolve: {task}")
    iac_layout = data.get("iac_layout") or {}
    if iac_layout.get("dev_path") == iac_layout.get("test_path"):
        errors.append(f"{rel(path, root)} iac_layout dev_path and test_path must differ")
    env = data.get("env_isolation") or {}
    if env.get("env_var_prefix_dev") == env.get("env_var_prefix_test"):
        errors.append(f"{rel(path, root)} env var prefixes must differ")
    if env.get("secret_path_dev") == env.get("secret_path_test"):
        errors.append(f"{rel(path, root)} secret paths must differ")
    for scenario in data.get("scenario_patterns") or []:
        record = patterns.get(scenario)
        if not record:
            errors.append(f"{rel(path, root)} scenario pattern does not resolve: {scenario}")
            continue
        if runtime_tier is not None and record.get("runtime_tier") != runtime_tier:
            errors.append(f"{rel(path, root)} scenario {scenario} runtime tier does not match manifest")
    if data.get("cloud_integration_test_strategy") not in TEST_STRATEGIES:
        errors.append(f"{rel(path, root)} cloud_integration_test_strategy is invalid")


if __name__ == "__main__":
    sys.exit(main())
