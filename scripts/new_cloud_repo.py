#!/usr/bin/env python3
"""Bootstrap a new cloud repo from accb templates and payload metadata."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from accb_payload import AccbUserError, build_payload, load_json, load_manifest, repo_root, validate_scaffoldable


EXIT_OK = 0
EXIT_USER = 1
EXIT_ENV = 2

PROVIDER_FUNCTION_DIR = {
    ("aws", "python"): "templates/function/aws-lambda/python",
    ("aws", "typescript"): "templates/function/aws-lambda/typescript",
    ("aws", "go"): "templates/function/aws-lambda/go",
    ("gcp", "python"): "templates/function/gcp-cloudfn/python",
    ("gcp", "typescript"): "templates/function/gcp-cloudfn/typescript",
    ("gcp", "go"): "templates/function/gcp-cloudfn/go",
    ("azure", "python"): "templates/function/azure-fn/python",
    ("azure", "typescript"): "templates/function/azure-fn/typescript",
    ("azure", "dotnet"): "templates/function/azure-fn/dotnet-isolated",
}

CONTAINER_DIR = {
    ("gcp", "python"): "templates/container/cloudrun/python-fastapi",
    ("gcp", "typescript"): "templates/container/cloudrun/typescript-hono",
    ("gcp", "go"): "templates/container/cloudrun/go-echo",
    ("aws", "python"): "templates/container/apprunner/python-fastapi",
    ("aws", "typescript"): "templates/container/apprunner/typescript-hono",
    ("aws", "go"): "templates/container/apprunner/go-echo",
    ("azure", "python"): "templates/container/aca/python-fastapi",
    ("azure", "typescript"): "templates/container/aca/typescript-hono",
    ("azure", "go"): "templates/container/aca/go-echo",
    ("azure", "dotnet"): "templates/container/aca/dotnet-aspnet",
}

K8S_PROVIDER = {"aws": "eks", "gcp": "gke", "azure": "aks"}
REGION = {"aws": "us-east-1", "gcp": "us-central1", "azure": "eastus"}


@dataclass(frozen=True)
class RenderedFile:
    source: Path | None
    target: Path
    content: str


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
    return slug or "accb-repo"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def template_target(template: Path, template_root: Path, args: argparse.Namespace) -> Path:
    rel = template.relative_to(template_root)
    parts = rel.parts
    if parts and parts[0] == "templates":
        parts = parts[1:]
    name = parts[-1].replace(".template", "")
    if parts[0] == "agent-md":
        return Path("AGENT.md")
    if parts[0] == "claude-md":
        return Path("CLAUDE.md")
    if parts[0] == "readme":
        return Path("README.md")
    if parts[0] == "prompt-first":
        return Path(".prompts") / name
    if parts[0] == "manifest":
        return Path("manifests") / name
    if parts[0] == "function":
        provider, lang = parts[1], parts[2]
        if provider == "aws-lambda":
            if lang == "python":
                return Path("src") / name
            if lang == "typescript":
                return Path("src") / name
            if lang == "go":
                return Path(name)
        return Path(*parts[3:-1]) / name if len(parts) > 4 else Path(name)
    if parts[0] == "container":
        return Path(*parts[3:-1]) / name if len(parts) > 4 else Path(name)
    if parts[0] == "k8s":
        if parts[1] == "helm-chart":
            return Path("charts") / args.target_dir.name / Path(*parts[2:-1]) / name
        return Path("k8s") / Path(*parts[2:-1]) / name
    if parts[0] == "iac":
        if parts[1] == "pulumi":
            return Path("iac/pulumi") / parts[2] / Path(*parts[4:-1]) / name
        if parts[1] == "terraform":
            return Path("iac/terraform") / Path(*parts[3:-1]) / name
    if parts[0] == "smoke-tests":
        return Path("tests/smoke") / name
    if parts[0] == "integration-tests":
        return Path("tests/integration") / name
    if parts[0] == "observability":
        return Path("observability") / name
    return Path(*parts[:-1]) / name


def gitignore_content(template_root: Path, language: str, iac_tool: str) -> str:
    fragments = ["base"]
    if language in {"python", "typescript", "go", "dotnet"}:
        fragments.append("node" if language == "typescript" else language)
    fragments.append("terraform" if iac_tool == "terraform" else "pulumi")
    chunks = []
    for fragment in fragments:
        path = template_root / "templates/gitignore" / f"{fragment}.gitignore.template"
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8").strip())
    return "\n\n".join(chunks) + "\n"


def render_plan(args: argparse.Namespace, manifest: dict[str, Any]) -> list[RenderedFile]:
    root = repo_root()
    target = args.target_dir.resolve()
    repo_name = target.name
    repo_slug = slugify(repo_name)
    env = manifest.get("env_isolation", {})
    iac_layout = manifest.get("iac_layout", {})
    values = {
        "repo_name": repo_name,
        "repo_slug": repo_slug,
        "archetype": args.archetype,
        "provider": args.provider,
        "runtime_tier": args.runtime_tier,
        "primary_language": args.primary_language,
        "iac_tool": args.iac_tool,
        "state_backend_dev": f"{iac_layout.get('state_backend', 'local')}:dev",
        "state_backend_test": f"{iac_layout.get('state_backend', 'local')}:test",
        "env_var_prefix_dev": env.get("env_var_prefix_dev", f"ACCB_{repo_slug.upper()}_DEV_"),
        "env_var_prefix_test": env.get("env_var_prefix_test", f"ACCB_{repo_slug.upper()}_TEST_"),
        "secret_path_dev": env.get("secret_path_dev", f"/accb/dev/{repo_slug}/"),
        "secret_path_test": env.get("secret_path_test", f"/accb/test/{repo_slug}/"),
        "primary_region_dev": REGION.get(args.provider, "local"),
        "primary_region_test": REGION.get(args.provider, "local"),
        "namespace_dev": f"{repo_slug}-dev",
        "namespace_test": f"{repo_slug}-test",
        "image_registry": f"{args.provider}.example.invalid",
        "image_repository": repo_slug,
        "image_tag": "dev",
    }
    files: list[RenderedFile] = []
    for rel in ("templates/agent-md", "templates/claude-md", "templates/readme", "templates/prompt-first"):
        add_templates(files, root, rel, values, args)
    files.append(RenderedFile(None, Path(".gitignore"), gitignore_content(root, args.primary_language, args.iac_tool)))
    files.append(RenderedFile(None, Path("PLAN.md"), f"# {repo_name} Plan\n\nGenerated starter. Keep validation current.\n"))

    if args.iac_tool == "terraform" and args.include_dev_test_pair:
        add_templates(files, root, f"templates/iac/terraform/{args.provider}", values, args)
    elif args.iac_tool.startswith("pulumi-"):
        language = args.iac_tool.removeprefix("pulumi-")
        add_templates(files, root, f"templates/iac/pulumi/{language}/{args.provider}", values, args)

    if args.runtime_tier == "function":
        add_templates(files, root, PROVIDER_FUNCTION_DIR.get((args.provider, args.primary_language), ""), values, args)
    elif args.runtime_tier == "managed_container":
        add_templates(files, root, CONTAINER_DIR.get((args.provider, args.primary_language), ""), values, args)
    elif args.runtime_tier == "k8s":
        provider_dir = K8S_PROVIDER.get(args.provider, args.provider)
        add_templates(files, root, f"templates/k8s/{provider_dir}", values, args)
        add_templates(files, root, "templates/k8s/helm-chart", values, args)

    if args.runtime_tier == "function":
        smoke = {"python": "function-smoke.py.template", "typescript": "function-smoke.ts.template", "go": "function-smoke.go.template"}.get(args.primary_language)
        if smoke:
            add_templates(files, root, f"templates/smoke-tests/{smoke}", values, args)
    elif args.runtime_tier == "managed_container":
        add_templates(files, root, "templates/smoke-tests/container-health-smoke.sh.template", values, args)
    elif args.runtime_tier == "k8s":
        add_templates(files, root, "templates/smoke-tests/k8s-pod-readiness-smoke.sh.template", values, args)

    if args.include_localstack_or_emulator:
        if args.provider == "aws":
            add_templates(files, root, "templates/integration-tests/localstack-compose.yaml.template", values, args)
        elif args.provider == "gcp":
            add_templates(files, root, "templates/integration-tests/gcp-emulators-compose.yaml.template", values, args)
        elif args.provider == "azure":
            add_templates(files, root, "templates/integration-tests/azurite-compose.yaml.template", values, args)
    if args.include_ephemeral_real_test:
        add_templates(files, root, "templates/integration-tests/terraform-apply-destroy.sh.template" if args.iac_tool == "terraform" else "templates/integration-tests/pulumi-up-down.py.template", values, args)

    if args.include_observability_bundle:
        add_templates(files, root, "templates/observability", values, args)
    add_templates(files, root, "templates/manifest", values, args)
    files.append(RenderedFile(root / "scripts/work.py", Path("scripts/work.py"), render((root / "scripts/work.py").read_text(encoding="utf-8"), values)))
    return sorted(files, key=lambda item: item.target.as_posix())


def add_templates(files: list[RenderedFile], root: Path, rel: str, values: dict[str, str], args: argparse.Namespace) -> None:
    path = root / rel
    if path.is_file():
        target = template_target(path, root, args)
        files.append(RenderedFile(path, target, render(path.read_text(encoding="utf-8"), values)))
    elif path.is_dir():
        for template in sorted(p for p in path.rglob("*") if p.is_file() and p.name != ".gitkeep"):
            target = template_target(template, root, args)
            files.append(RenderedFile(template, target, render(template.read_text(encoding="utf-8"), values)))


def validate_args(args: argparse.Namespace) -> dict[str, Any]:
    rules = load_json(repo_root() / "context/accb/profile-rules.json")
    scenario_map = load_yaml(repo_root() / "context/scenarios/scenario-profile-map.yaml")
    manifest = load_manifest(args.manifest)
    validate_scaffoldable(manifest)
    if args.archetype not in rules.get("archetype_capabilities", {}):
        raise AccbUserError(f"unknown archetype: {args.archetype}")
    if args.manifest not in rules.get("manifest_capabilities", {}):
        raise AccbUserError(f"unknown manifest: {args.manifest}")
    for service in args.support_services:
        if service not in rules.get("support_service_capabilities", {}):
            raise AccbUserError(f"unknown support service: {service}")
    for pattern in args.scenario_patterns or []:
        if pattern not in scenario_map.get("patterns", {}):
            raise AccbUserError(f"unknown scenario pattern: {pattern}")
    for field in ("archetype", "provider", "runtime_tier", "primary_stack", "primary_language", "iac_tool"):
        value = getattr(args, field)
        if manifest.get(field) and manifest[field] != value:
            raise AccbUserError(f"{field}={value!r} does not match manifest value {manifest[field]!r}")
    return manifest


def dry_run_output(files: list[RenderedFile], args: argparse.Namespace) -> str:
    lines = [
        f"accb new repo plan: {args.target_dir.resolve()}",
        f"profile: {args.archetype} | {args.provider} | {args.runtime_tier} | {args.primary_stack} | {args.iac_tool}",
        "write set:",
    ]
    lines.extend(f"- {item.target.as_posix()}" for item in files)
    lines.append("- .accb/")
    return "\n".join(lines) + "\n"


def write_repo(files: list[RenderedFile], args: argparse.Namespace) -> None:
    target = args.target_dir.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for item in files:
        dest = target / item.target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(item.content, encoding="utf-8")
    if args.initial_prompt_text or args.initial_prompt_file:
        prompt = args.initial_prompt_text
        if args.initial_prompt_file:
            prompt = Path(args.initial_prompt_file).read_text(encoding="utf-8")
        sentinel = target / ".accb/INITIAL_PROMPT.txt"
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text(prompt or "", encoding="utf-8")
    if not args.no_init_git and not (target / ".git").exists():
        subprocess.run(["git", "init", "-b", "main"], cwd=target, check=False, capture_output=True, text=True)


def next_steps(target: Path) -> str:
    return f"""
Next Steps
1. cd {target.resolve()}
2. git init -b main && git add . && git commit -m "initial scaffold"
3. python3 scripts/work.py resume
4. cat .accb/SESSION_BOOT.md
5. open .prompts/PROMPT_01.txt in a fresh session
""".strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a new accb cloud repo.")
    parser.add_argument("--archetype", required=True)
    parser.add_argument("--provider", choices=["aws", "gcp", "azure"], required=True)
    parser.add_argument("--runtime-tier", choices=["function", "managed_container", "k8s"], required=True)
    parser.add_argument("--primary-stack", required=True)
    parser.add_argument("--primary-language", required=True)
    parser.add_argument("--iac-tool", choices=["terraform", "pulumi-typescript", "pulumi-python", "pulumi-go", "pulumi-dotnet"], required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--scenario-pattern", action="append", dest="scenario_patterns")
    parser.add_argument("--support-service", action="append", default=[], dest="support_services")
    parser.add_argument("--include-dev-test-pair", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--include-localstack-or-emulator", action="store_true")
    parser.add_argument("--include-ephemeral-real-test", action="store_true")
    parser.add_argument("--include-secret-binding-example", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--include-observability-bundle", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--target-dir", required=True, type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--initial-prompt-text")
    group.add_argument("--initial-prompt-file")
    parser.add_argument("--include-startup-features", action="store_true")
    parser.add_argument("--no-init-git", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        manifest = validate_args(args)
        files = render_plan(args, manifest)
        if args.dry_run:
            print(dry_run_output(files, args), end="")
            return EXIT_OK
        write_repo(files, args)
        build_payload(
            archetype=args.archetype,
            primary_stack=args.primary_stack,
            primary_language=args.primary_language,
            provider=args.provider,
            runtime_tier=args.runtime_tier,
            iac_tool=args.iac_tool,
            manifest=args.manifest,
            support_services=args.support_services,
            scenario_patterns=args.scenario_patterns,
            target_root=args.target_dir,
            include_startup_features=args.include_startup_features,
        )
        print(next_steps(args.target_dir))
        return EXIT_OK
    except AccbUserError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_USER
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ENV


if __name__ == "__main__":
    raise SystemExit(main())
