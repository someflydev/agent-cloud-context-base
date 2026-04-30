#!/usr/bin/env python3
"""Compare candidate output against a canonical example."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


RESOURCE_RE = re.compile(r'\bresource\s+"([^"]+)"\s+"([^"]+)"|new\s+([A-Za-z0-9_.]+)')
HANDLER_RE = re.compile(r"\b(def|function|export\s+(?:async\s+)?function|func)\s+([A-Za-z_][A-Za-z0-9_]*)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Diff candidate implementation shape against a canonical example.")
    parser.add_argument("candidate_path")
    parser.add_argument("canonical_path")
    args = parser.parse_args(argv)
    candidate = Path(args.candidate_path).expanduser().resolve()
    canonical = Path(args.canonical_path).expanduser().resolve()
    if not candidate.exists() or not canonical.exists():
        print("candidate and canonical paths must both exist", file=sys.stderr)
        return 1
    categories = {
        "files": diff_sets(file_set(candidate), file_set(canonical)),
        "iac_resources": diff_sets(resource_set(candidate), resource_set(canonical)),
        "handler_signatures": diff_sets(handler_set(candidate), handler_set(canonical)),
        "manifest_fields": diff_sets(manifest_fields(candidate), manifest_fields(canonical)),
    }
    has_drift = False
    for category, (missing, extra) in categories.items():
        print(f"{category}:")
        if not missing and not extra:
            print("  no drift")
            continue
        has_drift = True
        for item in missing:
            print(f"  missing: {item}")
        for item in extra:
            print(f"  extra: {item}")
    return 1 if has_drift else 0


def file_set(path: Path) -> set[str]:
    if path.is_file():
        return {path.name}
    return {p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()}


def text_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return [p for p in path.rglob("*") if p.is_file() and p.suffix in {".tf", ".ts", ".py", ".go", ".cs", ".yaml", ".yml"}]


def resource_set(path: Path) -> set[str]:
    out: set[str] = set()
    for file_path in text_files(path):
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for match in RESOURCE_RE.finditer(text):
            out.add(":".join(group for group in match.groups() if group))
    return out


def handler_set(path: Path) -> set[str]:
    out: set[str] = set()
    for file_path in text_files(path):
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for match in HANDLER_RE.finditer(text):
            name = match.group(2)
            if "handler" in name.lower() or name in {"main", "run"}:
                out.add(name)
    return out


def manifest_fields(path: Path) -> set[str]:
    fields: set[str] = set()
    candidates = [path] if path.is_file() else list(path.rglob("*.yaml")) + list(path.rglob("*.yml"))
    for file_path in candidates:
        try:
            data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and ("schema_version" in data or "name" in data):
            fields.update(str(key) for key in data.keys())
    return fields


def diff_sets(candidate: set[str], canonical: set[str]) -> tuple[list[str], list[str]]:
    return sorted(canonical - candidate), sorted(candidate - canonical)


if __name__ == "__main__":
    sys.exit(main())
