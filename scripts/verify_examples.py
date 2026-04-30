#!/usr/bin/env python3
"""Verify registered examples and optionally update verification timestamps."""

from __future__ import annotations

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from validation_common import read_json, read_yaml, repo_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify canonical examples declared in the registry.")
    parser.add_argument("--family", help="only verify one family")
    parser.add_argument("--update-registry", action="store_true", help="write last verification status into registry")
    parser.add_argument("--parallel", type=int, default=1, help="number of examples to verify concurrently")
    args = parser.parse_args(argv)
    root = repo_root()
    registry_path = root / "verification/example_registry.yaml"
    registry = read_yaml(registry_path)
    catalog = read_json(root / "examples/catalog.json")
    entries = collect_examples(registry, catalog, args.family)
    if not entries:
        print("no examples registered")
        return 0
    workers = max(1, args.parallel)
    if workers == 1:
        results = [verify_one(root, entry) for entry in entries]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(lambda entry: verify_one(root, entry), entries))
    failed = [result for result in results if not result["ok"]]
    for result in results:
        status = "passed" if result["ok"] else "failed"
        print(f"{result['id']}: {status} ({result['message']})")
    if args.update_registry:
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        update_registry(registry, results, stamp)
        registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
    return 1 if failed else 0


def collect_examples(registry: dict[str, Any], catalog: dict[str, Any], family: str | None) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(registry, list):
        registry_entries = registry
    else:
        registry_entries = registry.get("examples") or registry.get("entries") or []
        for fam in registry.get("families") or []:
            if family and fam.get("name") != family:
                continue
            for example in fam.get("examples") or []:
                registry_entries.append({**example, "family": fam.get("name")})
    for example in registry_entries:
        if not isinstance(example, dict):
            continue
        if family and example.get("family") != family:
            continue
        entries.append(example)
    catalog_examples = catalog.get("examples") or []
    if family:
        catalog_examples = [entry for entry in catalog_examples if entry.get("family") == family]
    for example in catalog_examples:
        if not any(example_key(item) == example_key(example) for item in entries):
            entries.append(example)
    return entries


def example_key(entry: dict[str, Any]) -> str:
    return str(entry.get("id") or entry.get("name") or entry.get("path") or "")


def verify_one(root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    example_id = entry.get("id") or entry.get("name") or entry.get("path") or "unknown"
    for file_name in entry.get("files") or []:
        if not (root / file_name).exists():
            return {"id": example_id, "ok": False, "message": f"missing file {file_name}"}
    command = entry.get("verify_command")
    if not command:
        return {"id": example_id, "ok": True, "message": "no verify_command declared"}
    result = subprocess.run(command, cwd=root, shell=True, text=True, capture_output=True, timeout=300)
    message = result.stdout.strip() or result.stderr.strip() or f"exit {result.returncode}"
    return {"id": example_id, "ok": result.returncode == 0, "message": message[:200]}


def update_registry(registry: dict[str, Any], results: list[dict[str, Any]], stamp: str) -> None:
    by_id = {result["id"]: result for result in results}
    for fam in registry.get("families") or []:
        for example in fam.get("examples") or []:
            example_id = example.get("id") or example.get("name") or example.get("path")
            result = by_id.get(example_id)
            if result:
                example["last_verified_at"] = stamp
                example["last_verified_status"] = "passed" if result["ok"] else "failed"


if __name__ == "__main__":
    sys.exit(main())
