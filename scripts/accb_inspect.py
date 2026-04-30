#!/usr/bin/env python3
"""Inspect a generated repo-local `.accb/` payload."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def inspect(repo: Path) -> dict[str, Any]:
    accb = repo / ".accb"
    selection = load_json(accb / "profile/selection.json")
    matrix = load_json(accb / "validation/MATRIX.json")
    rules_path = accb / "source/context/accb/profile-rules.json"
    rules = load_json(rules_path) if rules_path.exists() else {}
    service_caps = rules.get("support_service_capabilities", {})
    buckets = {"default": [], "archetype": [], "stack": [], "capability": []}
    for gate_id, gate in matrix.get("gates", {}).items():
        for source in gate.get("sources", []):
            buckets.setdefault(source, []).append(gate_id)
    return {
        "repo": repo.as_posix(),
        "selection": selection,
        "support_service_capabilities": {
            service: service_caps.get(service, []) for service in selection.get("support_services", [])
        },
        "gate_sources": buckets,
    }


def print_tree(data: dict[str, Any]) -> None:
    selection = data["selection"]
    service_caps = data.get("support_service_capabilities", {})
    buckets = data["gate_sources"]
    print("Profile")
    print(f"├── archetype: {selection['archetype']}")
    print(f"├── primary_stack: {selection['primary_stack']} (language: {selection['primary_language']})")
    print(f"├── provider: {selection['provider']} | runtime_tier: {selection['runtime_tier']}")
    print(f"├── iac_tool: {selection['iac_tool']}")
    print(f"├── manifest: {selection['manifest']}")
    print("├── scenario_patterns")
    for item in selection.get("scenario_patterns", []):
        print(f"│   └── {item}")
    print("├── support_services")
    for item in selection.get("support_services", []):
        print(f"│   ├── {item} → capabilities: {service_caps.get(item, [])}")
    if not selection.get("support_services"):
        print("│   └── []")
    print("├── capabilities (union)")
    for item in selection.get("capabilities", []):
        print(f"│   └── {item}")
    print("├── doctrines (loaded by default)")
    for item in selection.get("doctrines", []):
        print(f"│   └── {item}")
    print("└── validation_gates")
    for source in ("default", "archetype", "stack", "capability"):
        print(f"    ├── {source} ({len(buckets.get(source, []))} gates)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect the `.accb/` payload in a generated repo.")
    parser.add_argument("--repo", default=".", help="Repo root containing `.accb/`.")
    parser.add_argument("--json", action="store_true", help="Print the same content as JSON.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo = Path(args.repo).resolve()
    try:
        data = inspect(repo)
    except FileNotFoundError as exc:
        print(f"missing .accb payload file: {exc.filename}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print_tree(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
