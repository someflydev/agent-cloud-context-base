#!/usr/bin/env python3
"""Compose generated repo-local `.accb/` payloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


EXIT_OK = 0
EXIT_USER = 1
EXIT_ENV = 2

SPEC_SOURCES = {
    "PRODUCT": "context/specs/product/base.md",
    "ARCHITECTURE": "context/specs/architecture/base.md",
    "AGENT_RULES": "context/specs/agent/base.md",
    "EVOLUTION": "context/specs/evolution/base.md",
    "VALIDATION": "context/validation/base.md",
}

REFERENCE_ONLY_MESSAGE = (
    "reference-only manifest: this arc only scaffolds single-provider runnable repos in v1; "
    "catalog/reference manifests should use the canonical IaC / observability / secrets / "
    "eventing materials from PROMPT_24"
)


@dataclass(frozen=True)
class PayloadResult:
    written_files: list[Path]
    selection: dict[str, Any]
    gates_total: int
    covered_capabilities: list[str]


class AccbUserError(Exception):
    pass


def repo_root() -> Path:
    here = Path(__file__).resolve()
    root = here.parents[1]
    if (root / "context/accb/profile-rules.json").exists():
        return root
    source_root = root / "source"
    if (source_root / "context/accb/profile-rules.json").exists():
        return source_root
    return root


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AccbUserError(f"missing required file: {path}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise AccbUserError(f"expected mapping in {path}")
    return data


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AccbUserError(f"missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def manifest_path(name: str) -> Path:
    return repo_root() / "manifests" / f"{name}.yaml"


def load_manifest(name: str) -> dict[str, Any]:
    path = manifest_path(name)
    if not path.exists():
        raise AccbUserError(f"unknown manifest: {name}")
    manifest = load_yaml(path)
    if manifest.get("name") and manifest["name"] != name:
        raise AccbUserError(f"manifest name mismatch: {name} != {manifest['name']}")
    return manifest


def validate_scaffoldable(manifest: dict[str, Any]) -> None:
    if manifest.get("generated_repo_target") is False:
        raise AccbUserError(REFERENCE_ONLY_MESSAGE)
    if manifest.get("provider") in (None, "multi"):
        raise AccbUserError(REFERENCE_ONLY_MESSAGE)
    if manifest.get("runtime_tier") in (None, "null"):
        raise AccbUserError(REFERENCE_ONLY_MESSAGE)
    if manifest.get("primary_stack") in (None, "none"):
        raise AccbUserError(REFERENCE_ONLY_MESSAGE)


def gate_key(gate: dict[str, Any]) -> str:
    gate_id = gate.get("id")
    if not isinstance(gate_id, str) or not gate_id:
        raise AccbUserError(f"validation gate missing id: {gate}")
    return gate_id


def normalize_gate(gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": gate_key(gate),
        "category": gate.get("category", "general"),
        "summary": gate.get("summary", ""),
        **({"command": gate["command"]} if gate.get("command") else {}),
        "command_hint": gate.get("command_hint", gate.get("summary", "")),
    }


def collect_gates(
    rules: dict[str, Any], archetype: str, primary_stack: str, capabilities: list[str]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    ordered: dict[str, dict[str, Any]] = {}
    matrix: dict[str, dict[str, Any]] = {}

    def add(source: str, gates: list[dict[str, Any]], capability: str | None = None) -> None:
        for raw in gates:
            gate = normalize_gate(raw)
            gid = gate["id"]
            if gid not in ordered:
                ordered[gid] = gate
                matrix[gid] = {**gate, "sources": [], "capabilities": []}
            if source not in matrix[gid]["sources"]:
                matrix[gid]["sources"].append(source)
            if capability and capability not in matrix[gid]["capabilities"]:
                matrix[gid]["capabilities"].append(capability)

    add("default", list(rules.get("default_validation_gates", [])))
    add("archetype", list((rules.get("archetype_validation_gates", {}) or {}).get(archetype, [])))
    add("stack", list((rules.get("stack_validation_gates", {}) or {}).get(primary_stack, [])))
    capability_gates = rules.get("capability_validation_gates", {}) or {}
    for capability in capabilities:
        add("capability", list(capability_gates.get(capability, [])), capability)
    return list(ordered.values()), matrix


def selected_patterns(
    scenario_map: dict[str, Any], pattern_ids: list[str], provider: str
) -> dict[str, Any]:
    patterns = scenario_map.get("patterns", {})
    selected: dict[str, Any] = {"schema_version": 1, "patterns": {}}
    for pattern_id in pattern_ids:
        record = patterns[pattern_id]
        selected["patterns"][pattern_id] = {
            "pattern_id": pattern_id,
            "runtime_tier": record.get("runtime_tier"),
            "archetype": record.get("archetype"),
            "likely_manifest": (record.get("likely_manifests") or {}).get(provider),
            "support_services": (record.get("support_services") or {}).get(provider, []),
            "preferred_examples": record.get("preferred_examples", []),
        }
    return selected


def write_text(path: Path, text: str, written: list[Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    written.append(path)


def write_json(path: Path, data: Any, written: list[Path]) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n", written)


def compose_spec(title: str, source_rel: str) -> str:
    source = repo_root() / source_rel
    body = source.read_text(encoding="utf-8")
    header = f"<!-- Generated by accb_payload.py from {source_rel}. -->"
    if body.startswith("---\n"):
        end = body.find("\n---\n", 4)
        if end != -1:
            frontmatter = body[: end + 5].strip()
            rest = body[end + 5 :].strip()
            return f"{frontmatter}\n\n{header}\n\n# {title}\n\n{rest}\n"
    return f"{header}\n\n# {title}\n\n{body.strip()}\n"


def checklist(gates: list[dict[str, Any]]) -> str:
    lines = ["# Validation Checklist", ""]
    for gate in gates:
        lines.append(f"- [ ] `{gate['id']}` ({gate.get('category', 'general')}): {gate.get('summary', '')}")
        lines.append(f"  - Command hint: {gate.get('command_hint', '')}")
    return "\n".join(lines) + "\n"


def coverage(capabilities: list[str], matrix: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    covered: list[str] = []
    missing: list[str] = []
    sources_by_capability: dict[str, list[str]] = {}
    for capability in capabilities:
        gate_ids = [
            gate_id
            for gate_id, gate in matrix.items()
            if capability in gate.get("capabilities", [])
        ]
        sources_by_capability[capability] = gate_ids
        if gate_ids:
            covered.append(capability)
        else:
            missing.append(capability)
    return {
        "schema_version": 1,
        "capabilities": {cap: {"covered": bool(sources_by_capability[cap]), "gates": sources_by_capability[cap]} for cap in capabilities},
        "summary": {"covered_capabilities": covered, "missing_capabilities": missing},
    }, covered


def session_boot(selection: dict[str, Any]) -> str:
    doctrines = "\n".join(f"- `{item}`" for item in selection.get("doctrines", []))
    return f"""# accb Session Boot

## Active Profile

- Archetype: `{selection['archetype']}`
- Provider: `{selection['provider']}`
- Runtime tier: `{selection['runtime_tier']}`
- Primary stack: `{selection['primary_stack']}`
- Primary language: `{selection['primary_language']}`
- IaC tool: `{selection['iac_tool']}`
- Manifest: `{selection['manifest']}`

## Required Boot Reads

1. `AGENT.md`
2. `README.md`
3. `.accb/profile/selection.json`
4. `.accb/profile/scenario-patterns.json`
5. `python3 scripts/work.py resume`

## Validation Path Reminder

Run `python .accb/scripts/accb_verify.py` before claiming completion. Exercise the changed cloud boundary directly.

## Routing Quick Reference

- Function work: inspect handler, trigger fixture, idempotency, and IaC binding.
- Container work: inspect image, health/readiness, service identity, and deployment config.
- Kubernetes work: inspect workload role separation, namespace policy, rollout, and IaC.
- IaC work: declare dev/test state, env-var prefix, secret path, and resource naming first.

## Default Doctrines

{doctrines}

## Stop Conditions Summary

Stop as `blocked` for missing credentials, quota, or unsafe cloud state. Stop as `incomplete` when validation was not run. Use `done` only after checks pass.
"""


def index_payload(accb_root: Path, written: list[Path], selection: dict[str, Any]) -> dict[str, Any]:
    files = []
    hashes: dict[str, str] = {}
    repo = accb_root.parent
    for path in sorted({p.resolve() for p in written}):
        rel = path.relative_to(repo).as_posix()
        if rel == ".accb/INDEX.json":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append({"path": rel, "size": path.stat().st_size, "sha256": digest})
        hashes[rel] = digest
    return {"schema_version": 1, "selection": selection, "files": files, "generated_file_hashes": hashes}


def copy_vendor_scripts(target_root: Path, written: list[Path]) -> None:
    script_dir = target_root / ".accb" / "scripts"
    script_dir.mkdir(parents=True, exist_ok=True)
    for name in ("accb_payload.py", "accb_inspect.py", "accb_verify.py"):
        source = repo_root() / "scripts" / name
        if not source.exists():
            source = Path(__file__).resolve().parent / name
        if source.exists():
            dest = script_dir / name
            if source.resolve() != dest.resolve():
                shutil.copy2(source, dest)
            written.append(dest)


def copy_source_bundle(target_root: Path, manifest: str, written: list[Path]) -> None:
    root = repo_root()
    rels = [
        "context/accb/profile-rules.json",
        "context/scenarios/scenario-profile-map.yaml",
        f"manifests/{manifest}.yaml",
        *SPEC_SOURCES.values(),
    ]
    for rel in unique(rels):
        source = root / rel
        if not source.exists():
            continue
        dest = target_root / ".accb/source" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != dest.resolve():
            shutil.copy2(source, dest)
        written.append(dest)


def build_payload(
    *,
    archetype: str,
    primary_stack: str,
    primary_language: str,
    provider: str,
    runtime_tier: str,
    iac_tool: str,
    manifest: str,
    support_services: list[str],
    scenario_patterns: list[str] | None = None,
    target_root: Path,
    include_startup_features: bool = False,
) -> PayloadResult:
    root = repo_root()
    rules = load_json(root / "context/accb/profile-rules.json")
    scenario_map = load_yaml(root / "context/scenarios/scenario-profile-map.yaml")
    manifest_data = load_manifest(manifest)
    validate_scaffoldable(manifest_data)

    if archetype not in rules.get("archetype_capabilities", {}):
        raise AccbUserError(f"unknown archetype: {archetype}")
    if manifest not in rules.get("manifest_capabilities", {}):
        raise AccbUserError(f"unknown manifest capabilities entry: {manifest}")
    if support_services:
        unknown_services = [s for s in support_services if s not in rules.get("support_service_capabilities", {})]
        if unknown_services:
            raise AccbUserError(f"unknown support service(s): {', '.join(unknown_services)}")

    patterns = list(scenario_patterns or manifest_data.get("scenario_patterns", []))
    scenario_records = scenario_map.get("patterns", {})
    unknown_patterns = [p for p in patterns if p not in scenario_records]
    if unknown_patterns:
        raise AccbUserError(f"unknown scenario pattern(s): {', '.join(unknown_patterns)}")

    for field, value in {
        "archetype": archetype,
        "primary_stack": primary_stack,
        "primary_language": primary_language,
        "provider": provider,
        "runtime_tier": runtime_tier,
        "iac_tool": iac_tool,
    }.items():
        manifest_value = manifest_data.get(field)
        if manifest_value and manifest_value != value:
            raise AccbUserError(f"{field}={value!r} does not match manifest value {manifest_value!r}")

    capabilities = unique(
        list(rules["archetype_capabilities"][archetype])
        + list(rules["manifest_capabilities"][manifest])
        + [cap for service in support_services for cap in rules["support_service_capabilities"][service]]
    )
    gates, matrix = collect_gates(rules, archetype, primary_stack, capabilities)
    selection = {
        "schema_version": 1,
        "archetype": archetype,
        "primary_stack": primary_stack,
        "primary_language": primary_language,
        "provider": provider,
        "runtime_tier": runtime_tier,
        "iac_tool": iac_tool,
        "manifest": manifest,
        "scenario_patterns": patterns,
        "support_services": support_services,
        "capabilities": capabilities,
        "doctrines": list(rules.get("default_doctrines", [])),
        "routers": list(rules.get("default_routers", [])),
        "anchors": list(rules.get("default_anchors", [])),
        "validation_gates": gates,
        "startup_features": {
            "budget_report_enabled": include_startup_features,
            "startup_trace_enabled": include_startup_features,
            "route_check_enabled": include_startup_features,
        },
    }

    target_root = target_root.resolve()
    accb = target_root / ".accb"
    written: list[Path] = []
    write_json(accb / "profile/selection.json", selection, written)
    write_json(accb / "profile/scenario-patterns.json", selected_patterns(scenario_map, patterns, provider), written)
    for title, source in SPEC_SOURCES.items():
        write_text(accb / "specs" / f"{title}.md", compose_spec(title.replace("_", " ").title(), source), written)
    write_text(accb / "validation/CHECKLIST.md", checklist(gates), written)
    write_json(accb / "validation/MATRIX.json", {"schema_version": 1, "gates": matrix}, written)
    coverage_doc, covered = coverage(capabilities, matrix)
    write_json(accb / "validation/COVERAGE.json", coverage_doc, written)
    write_text(accb / "SESSION_BOOT.md", session_boot(selection), written)
    copy_source_bundle(target_root, manifest, written)
    copy_vendor_scripts(target_root, written)
    index = index_payload(accb, written, selection)
    write_json(accb / "INDEX.json", index, written)
    index = index_payload(accb, written, selection)
    write_json(accb / "INDEX.json", index, [])
    return PayloadResult(written, selection, len(gates), covered)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compose a generated repo `.accb/` payload.")
    parser.add_argument("--archetype", required=True)
    parser.add_argument("--primary-stack", required=True)
    parser.add_argument("--primary-language", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--runtime-tier", required=True)
    parser.add_argument("--iac-tool", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--scenario-pattern", action="append", dest="scenario_patterns")
    parser.add_argument("--support-service", action="append", default=[], dest="support_services")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--include-startup-features", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = build_payload(
            archetype=args.archetype,
            primary_stack=args.primary_stack,
            primary_language=args.primary_language,
            provider=args.provider,
            runtime_tier=args.runtime_tier,
            iac_tool=args.iac_tool,
            manifest=args.manifest,
            support_services=args.support_services,
            scenario_patterns=args.scenario_patterns,
            target_root=Path(args.output_dir),
            include_startup_features=args.include_startup_features,
        )
    except AccbUserError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_USER
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ENV
    print(f"wrote {len(result.written_files)} payload files to {Path(args.output_dir).resolve() / '.accb'}")
    print(f"validation gates: {result.gates_total}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
