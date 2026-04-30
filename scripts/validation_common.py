#!/usr/bin/env python3
"""Shared helpers for accb validation scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path, root: Path | None = None) -> str:
    base = root or repo_root()
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def file_stems(directory: Path, suffix: str = ".md") -> set[str]:
    return {path.stem for path in directory.glob(f"*{suffix}") if path.is_file()}


def path_exists_or_planned(root: Path, entry: str) -> bool:
    if not entry:
        return False
    path = root / entry
    if path.exists():
        return True
    planned_prefixes = (
        "examples/canonical-",
        "examples/canonical_",
        "templates/function/",
        "templates/container/",
        "templates/iac/pulumi/",
        "templates/iac/terraform/",
        "templates/k8s/",
    )
    return entry.startswith(planned_prefixes)


def print_report(title: str, errors: list[str], warnings: list[str]) -> int:
    if errors:
        print(f"{title}: failed")
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print(f"{title}: passed")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 1 if errors else 0
