#!/usr/bin/env python3
"""Check scenario profile map coverage."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(f"scenario check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    path = ROOT / "context/scenarios/scenario-profile-map.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    patterns: dict[str, Any] = data.get("patterns") or {}
    if not patterns:
        fail("no scenario patterns declared")
    manifests = {p.stem for p in (ROOT / "manifests").glob("*.yaml")}
    archetypes = {p.stem for p in (ROOT / "context/archetypes").glob("*.md")}
    for name, pattern in patterns.items():
        if pattern.get("archetype") not in archetypes:
            fail(f"{name} unresolved archetype {pattern.get('archetype')!r}")
        likely = pattern.get("likely_manifests") or {}
        if not likely:
            fail(f"{name} missing likely_manifests")
        for provider, manifest in likely.items():
            if manifest not in manifests:
                fail(f"{name} provider {provider} unresolved manifest {manifest!r}")
        support = pattern.get("support_services") or {}
        if not support or not all(support.get(provider) for provider in support):
            fail(f"{name} missing support services")
        examples = pattern.get("preferred_examples") or []
        existing = [example for example in examples if (ROOT / example).exists()]
        if not existing and not pattern.get("examples_deferred"):
            fail(f"{name} has no existing canonical example and no examples_deferred marker")
    print(f"scenario parity ok: {len(patterns)} patterns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
