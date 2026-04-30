#!/usr/bin/env python3
"""Validate accb context integrity."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from validation_common import read_json, read_yaml, repo_root, rel


LEGACY_TOKEN = "a" + "cb"
FORBIDDEN_RE = re.compile(rf"\b{LEGACY_TOKEN}\b|\.{LEGACY_TOKEN}/")
FRONTMATTER_REQUIRED = {"accb_origin", "accb_source_path", "accb_role", "accb_version"}
WORKFLOW_PATH_RE = re.compile(r"context/workflows/([A-Za-z0-9_.-]+)\.md")
STACK_PATH_RE = re.compile(r"context/stacks/([A-Za-z0-9_.-]+)\.md")
PROMPT_RE = re.compile(r"PROMPT_(\d+)\.txt$")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate context files, references, and prompt numbering.")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)
    root = repo_root()
    errors: list[str] = []
    warnings: list[str] = []

    validate_frontmatter(root, errors)
    validate_forbidden_terms(root, errors)
    validate_profile_refs(root, errors)
    validate_content_refs(root, errors)
    validate_prompt_numbering(root, errors)
    validate_scenarios(root, errors, warnings)

    if args.strict and warnings:
        errors.extend(warnings)
        warnings = []
    if errors:
        print("context validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARN: {warning}")
        return 1
    print("context validation passed")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


def validate_frontmatter(root: Path, errors: list[str]) -> None:
    for base in (root / "context/specs", root / "context/validation"):
        for path in sorted(base.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            if not text.startswith("---\n"):
                errors.append(f"{rel(path, root)} missing frontmatter")
                continue
            end = text.find("\n---\n", 4)
            if end == -1:
                errors.append(f"{rel(path, root)} has unterminated frontmatter")
                continue
            data = read_yaml_fragment(text[4:end], path, errors)
            missing = FRONTMATTER_REQUIRED - set(data)
            if missing:
                errors.append(f"{rel(path, root)} missing frontmatter fields {sorted(missing)}")


def read_yaml_fragment(text: str, path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        data = read_yaml_text(text)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{rel(path)} frontmatter does not parse: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{rel(path)} frontmatter must be a mapping")
        return {}
    return data


def read_yaml_text(text: str) -> Any:
    import yaml

    return yaml.safe_load(text) or {}


def validate_forbidden_terms(root: Path, errors: list[str]) -> None:
    for path in sorted((root / "context").rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if FORBIDDEN_RE.search(line):
                errors.append(f"{rel(path, root)}:{number} contains forbidden legacy token")


def validate_profile_refs(root: Path, errors: list[str]) -> None:
    rules = read_json(root / "context/accb/profile-rules.json")
    check_names(root, errors, "doctrine", rules.get("default_doctrines", []), "context/doctrine")
    check_names(root, errors, "doctrine", list((rules.get("doctrine_module_map") or {}).keys()), "context/doctrine")
    for name in rules.get("default_routers", []):
        if not (root / "context/router" / f"{name}.md").exists() and not (root / "context/router" / f"{name}.json").exists() and not (root / "context/router" / f"{name}.yaml").exists():
            errors.append(f"router {name!r} does not resolve under context/router/")
    check_names(root, errors, "anchor", rules.get("default_anchors", []), "context/anchors")
    check_names(root, errors, "archetype", list((rules.get("archetype_capabilities") or {}).keys()), "context/archetypes")


def check_names(root: Path, errors: list[str], label: str, names: list[str], folder: str) -> None:
    for name in names:
        if not (root / folder / f"{name}.md").exists():
            errors.append(f"{label} {name!r} does not resolve under {folder}/")


def validate_content_refs(root: Path, errors: list[str]) -> None:
    workflow_names = {path.stem for path in (root / "context/workflows").glob("*.md")}
    stack_names = {path.stem for path in (root / "context/stacks").glob("*.md")}
    sources = list((root / "context/router").glob("*")) + list((root / "context/archetypes").glob("*.md")) + list((root / "context/skills").glob("*.md"))
    for path in sources:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in WORKFLOW_PATH_RE.finditer(text):
            name = match.group(1)
            if name not in workflow_names:
                errors.append(f"{rel(path, root)} references missing workflow {name!r}")
        for match in STACK_PATH_RE.finditer(text):
            name = match.group(1)
            if name not in stack_names and name != "none":
                errors.append(f"{rel(path, root)} references missing stack {name!r}")
    for path in sorted((root / "manifests").glob("*.yaml")):
        data = read_yaml(path)
        for name in data.get("task_hints") or []:
            if name not in workflow_names:
                errors.append(f"{rel(path, root)} references missing workflow {name!r}")
        for name in [data.get("primary_stack"), *(data.get("secondary_stacks") or [])]:
            if name and name not in stack_names and name != "none":
                errors.append(f"{rel(path, root)} references missing stack {name!r}")


def validate_prompt_numbering(root: Path, errors: list[str]) -> None:
    for directory in (root / ".prompts", root / "examples/canonical-prompts"):
        numbers: list[int] = []
        for path in directory.glob("PROMPT_*.txt"):
            match = PROMPT_RE.search(path.name)
            if match:
                numbers.append(int(match.group(1)))
        if not numbers:
            continue
        expected = list(range(min(numbers), max(numbers) + 1))
        if sorted(numbers) != expected or len(numbers) != len(set(numbers)):
            errors.append(f"{rel(directory, root)} prompt numbering has gaps or duplicates")


def validate_scenarios(root: Path, errors: list[str], warnings: list[str]) -> None:
    data = read_yaml(root / "context/scenarios/scenario-profile-map.yaml")
    patterns = data.get("patterns") or {}
    manifests = {path.stem for path in (root / "manifests").glob("*.yaml")}
    archetypes = {path.stem for path in (root / "context/archetypes").glob("*.md")}
    support = set((read_json(root / "context/accb/profile-rules.json").get("support_service_capabilities") or {}).keys())
    for name, record in patterns.items():
        if record.get("archetype") not in archetypes:
            errors.append(f"scenario {name!r} archetype does not resolve")
        for provider, manifest in (record.get("likely_manifests") or {}).items():
            if manifest not in manifests:
                errors.append(f"scenario {name!r} manifest for {provider} does not resolve: {manifest}")
        for provider, services in (record.get("support_services") or {}).items():
            for service in services or []:
                if service not in support:
                    errors.append(f"scenario {name!r} support service for {provider} does not resolve: {service}")
        for example in record.get("preferred_examples") or []:
            if not (root / example).exists():
                warnings.append(f"scenario {name!r} preferred example not present yet: {example}")


if __name__ == "__main__":
    sys.exit(main())
