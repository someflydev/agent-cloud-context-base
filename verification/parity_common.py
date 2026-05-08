#!/usr/bin/env python3
"""Shared parity checks for canonical accb examples."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


VALID_STATUSES = {"pending", "passed", "failed", "skipped", "blocked", "incomplete"}
LOG_FIELD_SIGNALS = ("trace_id", "correlation_id", "request_id", "event_id", "environment")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def registry_entries(root: Path, families: set[str]) -> list[dict[str, Any]]:
    registry = load_yaml(root / "verification/example_registry.yaml")
    entries: list[dict[str, Any]] = []
    for family in registry.get("families") or []:
        name = family.get("name")
        if name not in families:
            continue
        for example in family.get("examples") or []:
            entries.append({**example, "family": name})
    return entries


def catalog_entries(root: Path, families: set[str]) -> list[dict[str, Any]]:
    catalog = load_json(root / "examples/catalog.json")
    return [entry for entry in catalog.get("examples") or [] if entry.get("family") in families]


def fail(message: str) -> None:
    print(f"parity check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def entry_key(entry: dict[str, Any]) -> tuple[str, str, str]:
    return (str(entry.get("family")), str(entry.get("name")), str(entry.get("language")))


def assert_catalog_matches(root: Path, entries: list[dict[str, Any]]) -> None:
    catalog_by_key = {entry_key(entry): entry for entry in catalog_entries(root, {e["family"] for e in entries})}
    for entry in entries:
        catalog = catalog_by_key.get(entry_key(entry))
        if not catalog:
            fail(f"missing catalog entry for {entry_key(entry)}")
        for field in ("provider", "runtime_tier", "language"):
            if str(entry.get(field)) != str(catalog.get(field)):
                fail(f"catalog mismatch for {entry_key(entry)} field {field}")
        if catalog.get("path") and not (root / catalog["path"]).exists():
            fail(f"catalog path missing: {catalog['path']}")


def assert_expected_layout(root: Path, entry: dict[str, Any]) -> Path:
    path = catalog_path(root, entry)
    if entry.get("runtime_tier") == "iac":
        if not (path / "README.md").exists():
            fail(f"{path.relative_to(root)} missing README.md")
        if not ((path / "dev").exists() and (path / "test").exists()) and not (
            (path / "Pulumi.dev.yaml").exists() and (path / "Pulumi.test.yaml").exists()
        ):
            fail(f"{path.relative_to(root)} missing dev/test IaC layout")
        return path
    required = ["README.md", "catalog-entry.json", "tests/verify.sh"]
    if entry.get("runtime_tier") in {"function", "managed_container", "k8s"}:
        required.append("observability/structured-log-shape.md")
    for rel in required:
        if not (path / rel).exists():
            fail(f"{path.relative_to(root)} missing {rel}")
    if not (path / "src").exists() and not (path / "k8s").exists() and not any(path.glob("*.tf")):
        fail(f"{path.relative_to(root)} missing source or platform layout")
    return path


def catalog_path(root: Path, entry: dict[str, Any]) -> Path:
    catalog_by_key = {entry_key(item): item for item in catalog_entries(root, {entry["family"]})}
    catalog = catalog_by_key.get(entry_key(entry))
    if catalog and catalog.get("path"):
        return root / catalog["path"]
    return root / "examples" / str(entry["family"]) / str(entry["name"]) / str(entry["language"])


def assert_structured_log_shape(path: Path, root: Path) -> None:
    log_shape = path / "observability/structured-log-shape.md"
    if not log_shape.exists():
        return
    text = log_shape.read_text(encoding="utf-8", errors="replace")
    if not any(field in text for field in LOG_FIELD_SIGNALS):
        fail(f"{log_shape.relative_to(root)} missing required structured log field signals")


def assert_registry_verification(entry: dict[str, Any]) -> None:
    verification = entry.get("verification")
    if not isinstance(verification, dict):
        fail(f"{entry_key(entry)} missing verification map")
    required = ["smoke"]
    if entry.get("verify_command_local_provider"):
        required.append("local_provider")
    if entry.get("verify_command_real_cloud"):
        required.append("real_cloud")
    if entry.get("verify_command_full"):
        required.append("full")
    for tier in required:
        meta = verification.get(tier)
        if not isinstance(meta, dict):
            fail(f"{entry_key(entry)} missing verification.{tier}")
        status = meta.get("status")
        if status not in VALID_STATUSES:
            fail(f"{entry_key(entry)} has invalid {tier} status {status!r}")
        if "command" not in meta:
            fail(f"{entry_key(entry)} verification.{tier} missing command")
        if status in {"passed", "failed"} and not meta.get("verified_at"):
            fail(f"{entry_key(entry)} verification.{tier} missing verified_at")
        if status in {"skipped", "blocked", "incomplete"} and not meta.get("reason"):
            fail(f"{entry_key(entry)} verification.{tier} missing reason")
        if tier in {"local_provider", "real_cloud"} and not (meta.get("lane") or meta.get("provider") or meta.get("cost")):
            fail(f"{entry_key(entry)} verification.{tier} missing lane/provider metadata")


def assert_iac_isolation(root: Path, path: Path) -> None:
    iac = path / "iac"
    roots: list[Path] = []
    if iac.exists():
        terraform = iac / "terraform"
        if terraform.exists():
            roots.append(terraform)
        pulumi = iac / "pulumi"
        if pulumi.exists():
            roots.extend(
                child
                for child in pulumi.iterdir()
                if child.is_dir() and ((child / "Pulumi.dev.yaml").exists() or list(child.glob("*.tf")))
            )
    elif "canonical-iac-terraform" in path.parts or "canonical-iac-pulumi" in path.parts:
        roots.append(path)
    for iac_root in roots:
        result = subprocess.run(
            ["python3", "scripts/validate_iac_isolation.py", str(iac_root)],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            detail = result.stdout.strip() or result.stderr.strip()
            fail(f"IaC isolation failed for {iac_root.relative_to(root)}: {detail.splitlines()[-1] if detail else 'no detail'}")


def run_family_parity(families: set[str]) -> int:
    root = repo_root()
    entries = registry_entries(root, families)
    if not entries:
        fail(f"no registry entries for {', '.join(sorted(families))}")
    assert_catalog_matches(root, entries)
    for entry in entries:
        path = assert_expected_layout(root, entry)
        assert_iac_isolation(root, path)
        assert_structured_log_shape(path, root)
        assert_registry_verification(entry)
    print(f"parity ok: {len(entries)} entries across {', '.join(sorted(families))}")
    return 0
