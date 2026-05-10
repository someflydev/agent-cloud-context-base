#!/usr/bin/env python3
"""Render docs/provider-parity-matrix.md from stack_support_matrix.yaml."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "verification/stack_support_matrix.yaml"
OUTPUT_PATH = ROOT / "docs/provider-parity-matrix.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render provider parity matrix documentation.")
    parser.add_argument("--check", action="store_true", help="verify the rendered document is current")
    args = parser.parse_args(argv)
    rendered = render()
    if args.check:
        current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if current != rendered:
            print(f"{OUTPUT_PATH.relative_to(ROOT)} is out of sync", file=sys.stderr)
            return 1
        print(f"{OUTPUT_PATH.relative_to(ROOT)} is in sync")
        return 0
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


def render() -> str:
    matrix = yaml.safe_load(MATRIX_PATH.read_text(encoding="utf-8")) or {}
    catalog = load_catalog()
    lines = [
        "# Provider Parity Matrix",
        "",
        "Generated from `verification/stack_support_matrix.yaml` by `scripts/render_parity_matrix.py`.",
        "",
        "| Provider | Runtime tier | Platform / tool | Language / variant | Status | Canonical example | Follow-up |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in flatten(matrix.get("matrix") or {}, catalog):
        lines.append(
            "| {provider} | {runtime} | {platform} | {variant} | {status} | {example} | {follow_up} |".format(
                **row
            )
        )
    lines.append("")
    return "\n".join(lines)


def load_catalog() -> list[dict[str, str]]:
    import json

    path = ROOT / "examples/catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        {
            "family": str(entry.get("family")),
            "name": str(entry.get("name")),
            "language": str(entry.get("language", "")),
            "path": str(entry.get("path")),
        }
        for entry in data.get("examples") or []
        if entry.get("family") and entry.get("name") and entry.get("path")
    ]


def flatten(matrix: dict[str, Any], catalog: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for provider, runtime_map in matrix.items():
        for runtime, platform_map in runtime_map.items():
            for platform, variant_map in platform_map.items():
                if not isinstance(variant_map, dict):
                    continue
                for variant, meta in variant_map.items():
                    if not isinstance(meta, dict):
                        continue
                    status = str(meta.get("status", "unknown"))
                    family = meta.get("family")
                    example = meta.get("example")
                    example_link = ""
                    if family and example:
                        path = resolve_catalog_path(catalog, str(family), str(example), str(variant))
                        example_link = f"[{family}/{example}](../{path}/)"
                    follow_up = ""
                    if status == "deferred":
                        follow_up = meta.get("follow_up") or meta.get("reason") or "follow-up arc deferred"
                    elif status == "not-planned":
                        follow_up = meta.get("reason") or "not planned"
                    rows.append(
                        {
                            "provider": str(provider),
                            "runtime": str(runtime),
                            "platform": str(platform),
                            "variant": str(variant),
                            "status": status_to_label(status),
                            "example": example_link,
                            "follow_up": str(follow_up),
                        }
                    )
    return rows


def resolve_catalog_path(catalog: list[dict[str, str]], family: str, example: str, variant: str) -> str:
    candidates = [entry for entry in catalog if entry["family"] == family and entry["name"] == example]
    if not candidates:
        return f"examples/{family}/{example}"
    if len(candidates) == 1:
        return candidates[0]["path"]

    normalized_variant = variant.replace("_", "-")
    for entry in candidates:
        language = entry["language"].replace("_", "-")
        path_tail = Path(entry["path"]).name.replace("_", "-")
        if normalized_variant in {language, path_tail}:
            return entry["path"]
        if normalized_variant.startswith(f"{language}-") or normalized_variant.startswith(f"{path_tail}-"):
            return entry["path"]

    return candidates[0]["path"]


def status_to_label(status: str) -> str:
    return {
        "supported": "Supported",
        "deferred": "Deferred",
        "not-planned": "Not Planned",
    }.get(status, status)


if __name__ == "__main__":
    raise SystemExit(main())
