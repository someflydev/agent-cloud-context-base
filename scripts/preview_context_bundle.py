#!/usr/bin/env python3
"""Preview a budget-aware first-pass context bundle for a manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validation_common import read_json, read_yaml, repo_root


PROFILE_LIMITS = {"tiny": 6, "small": 10, "medium": 16, "large": 24, "cross-cloud": 30}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preview the selected context bundle for a manifest.")
    parser.add_argument("manifest_name", help="manifest name")
    parser.add_argument("--profile", choices=tuple(PROFILE_LIMITS), default="small")
    parser.add_argument("--show-weights", action="store_true")
    parser.add_argument("--show-anchors", action="store_true")
    parser.add_argument("--explain", action="store_true")
    args = parser.parse_args(argv)
    root = repo_root()
    rules = read_json(root / "context/accb/profile-rules.json")
    if not (rules.get("startup_features") or {}).get("budget_report_enabled", False):
        print("feature gated off in profile-rules.json")
        return 0
    path = root / "manifests" / f"{args.manifest_name}.yaml"
    if not path.exists():
        print(f"unknown manifest: {args.manifest_name}", file=sys.stderr)
        return 1
    manifest = read_yaml(path)
    bundle = build_bundle(manifest)
    limit = PROFILE_LIMITS[args.profile]
    selected = bundle[:limit]
    print(f"Manifest: {manifest.get('name')}")
    print(f"Profile: {args.profile} ({len(selected)}/{len(bundle)} entries)")
    for index, entry in enumerate(selected, start=1):
        suffix = " [required]" if entry in (manifest.get("required_context") or []) else " [optional]" if args.show_weights else ""
        print(f"{index}. {entry}{suffix}")
    if args.show_anchors:
        for anchor in rules.get("default_anchors") or []:
            print(f"anchor: context/anchors/{anchor}.md")
    if args.explain:
        print("Bundle order favors manifest required context, selected optional context, scenarios, and validation base.")
    return 0


def build_bundle(manifest: dict) -> list[str]:
    entries: list[str] = []
    for item in manifest.get("required_context") or []:
        add(entries, item)
    for item in manifest.get("optional_context") or []:
        add(entries, item)
    add(entries, "context/validation/base.md")
    add(entries, "context/doctrine/context-complexity-budget-cloud.md")
    return entries


def add(entries: list[str], item: str) -> None:
    if item and item not in entries:
        entries.append(item)


if __name__ == "__main__":
    sys.exit(main())
