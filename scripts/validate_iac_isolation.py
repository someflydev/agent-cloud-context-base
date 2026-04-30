#!/usr/bin/env python3
"""Validate dev/test IaC isolation for Terraform and Pulumi trees."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


EXIT_OK = 0
EXIT_USER = 1
EXIT_ENV = 2

SECRET_VALUE_RE = re.compile(
    r'(password|secret_key|client_secret|access_key)\s*=\s*"[^"$][^"]{7,}"|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|BEGIN PRIVATE KEY'
)
SECRET_REF_RE = re.compile(
    r'(?:data\.)?(?:aws_secretsmanager_secret|aws_ssm_parameter|google_secret_manager_secret_version|azurerm_key_vault_secret)[^"\n]*"([^"]+)"'
)
DEFAULT_CREDS_RE = re.compile(r'profile\s*=\s*"default"|AWS_PROFILE\s*=\s*"default"|GOOGLE_APPLICATION_CREDENTIALS|AzureCliCredential\(')
RESOURCE_RE = re.compile(r'\bresource\s+"[^"]+"\s+"([^"]+)"|new\s+[A-Za-z0-9_.]*Resource\(|pulumi\.(?:Custom)?Resource\(|new\s+azure\.|new\s+aws\.|new\s+gcp\.')
ENV_SIGNAL_RE = re.compile(r"var\.environment|pulumi\.getStack\(\)|StackName|Deployment\.Instance\.StackName|stack_name|get_stack\(\)|getStack")
BACKEND_VALUE_RE = re.compile(r'\b(key|prefix|path)\s*=\s*"([^"]+)"')


@dataclass
class Rule:
    rule_id: str
    status: str
    message: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Terraform or Pulumi dev/test isolation.")
    parser.add_argument("iac_root_dir", help="IaC root directory")
    parser.add_argument("--allow", action="append", default=[], help="suppress a rule id with an operator-documented reason")
    args = parser.parse_args(argv)
    root = Path(args.iac_root_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"IaC root does not exist or is not a directory: {root}", file=sys.stderr)
        return EXIT_ENV
    allowed = {item.split(":", 1)[0].strip() for item in args.allow}
    rules = validate(root)
    failed = False
    print(f"{'rule':34} {'status':8} message")
    print("-" * 80)
    for rule in rules:
        status = "allowed" if rule.rule_id in allowed and rule.status == "fail" else rule.status
        if status == "fail":
            failed = True
        print(f"{rule.rule_id:34} {status:8} {rule.message}")
    return EXIT_USER if failed else EXIT_OK


def validate(root: Path) -> list[Rule]:
    if (root / "dev").exists() or (root / "test").exists() or list(root.rglob("*.tf")):
        return validate_terraform(root)
    if list(root.glob("Pulumi.*.yaml")) or list(root.rglob("Pulumi.*.yaml")):
        return validate_pulumi(root)
    return [Rule("iac-layout", "fail", "no Terraform or Pulumi layout detected")]


def validate_terraform(root: Path) -> list[Rule]:
    rules: list[Rule] = []
    dev = root / "dev"
    test = root / "test"
    if test.exists() and dev.exists():
        rules.append(Rule("dev-test-layout", "pass", "dev and test Terraform trees exist"))
    elif test.exists():
        rules.append(Rule("dev-test-layout", "warn", "dev tree missing; test tree exists"))
    else:
        rules.append(Rule("dev-test-layout", "fail", "test Terraform tree is required"))
    backend_rule(root, dev, test, rules)
    source_rules(root, rules)
    secret_disjoint_rule(dev, test, rules)
    checked_in_state_rule(root, rules)
    return rules


def backend_rule(root: Path, dev: Path, test: Path, rules: list[Rule]) -> None:
    dev_backend = dev / "backend.tf"
    test_backend = test / "backend.tf"
    if not dev_backend.exists() or not test_backend.exists():
        rules.append(Rule("state-backend-disjoint", "fail", "dev/test backend.tf files are required"))
        return
    dev_text = dev_backend.read_text(encoding="utf-8", errors="replace")
    test_text = test_backend.read_text(encoding="utf-8", errors="replace")
    if "backend" not in dev_text or "backend" not in test_text:
        rules.append(Rule("state-backend-disjoint", "fail", "backend blocks are required in both envs"))
        return
    dev_key = backend_value(dev_text)
    test_key = backend_value(test_text)
    if dev_key and test_key and dev_key != test_key:
        rules.append(Rule("state-backend-disjoint", "pass", "state keys or prefixes differ"))
    else:
        rules.append(Rule("state-backend-disjoint", "fail", "state key or prefix must differ between dev and test"))


def backend_value(text: str) -> str | None:
    match = BACKEND_VALUE_RE.search(text)
    return match.group(2) if match else None


def validate_pulumi(root: Path) -> list[Rule]:
    rules: list[Rule] = []
    dev = root / "Pulumi.dev.yaml"
    test = root / "Pulumi.test.yaml"
    if dev.exists() and test.exists():
        rules.append(Rule("dev-test-layout", "pass", "flat Pulumi dev/test stacks exist"))
    else:
        nested = list(root.rglob("Pulumi.dev.yaml")) and list(root.rglob("Pulumi.test.yaml"))
        status = "warn" if nested else "fail"
        rules.append(Rule("dev-test-layout", status, "flat Pulumi stack files missing"))
    if dev.exists() and test.exists():
        dev_text = dev.read_text(encoding="utf-8", errors="replace")
        test_text = test.read_text(encoding="utf-8", errors="replace")
        dev_name = stack_name(dev_text, "dev")
        test_name = stack_name(test_text, "test")
        dev_backend = backend_value(dev_text)
        test_backend = backend_value(test_text)
        if dev_name != test_name and (not dev_backend or not test_backend or dev_backend != test_backend):
            rules.append(Rule("state-backend-disjoint", "pass", "Pulumi stack names and backend paths are disjoint"))
        else:
            rules.append(Rule("state-backend-disjoint", "fail", "Pulumi stack names or backend paths overlap"))
    source_rules(root, rules)
    pulumi_secret_disjoint_rule(dev, test, rules)
    checked_in_state_rule(root, rules)
    return rules


def stack_name(text: str, fallback: str) -> str:
    match = re.search(r"^\s*stack\s*:\s*(\S+)", text, flags=re.M)
    if match:
        return match.group(1)
    return fallback


def source_rules(root: Path, rules: list[Rule]) -> None:
    source_files = [p for pattern in ("*.tf", "*.tfvars", "*.ts", "*.py", "*.go", "*.cs") for p in root.rglob(pattern)]
    collision_hits: list[str] = []
    secret_hits: list[str] = []
    default_cred_hits: list[str] = []
    for path in source_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if RESOURCE_RE.search(text) and not ENV_SIGNAL_RE.search(text):
            collision_hits.append(path.relative_to(root).as_posix())
        if SECRET_VALUE_RE.search(text):
            secret_hits.append(path.relative_to(root).as_posix())
        if DEFAULT_CREDS_RE.search(text):
            default_cred_hits.append(path.relative_to(root).as_posix())
    if collision_hits:
        rules.append(Rule("resource-name-env-suffixed", "fail", f"resources lack env signal: {', '.join(collision_hits[:5])}"))
    else:
        rules.append(Rule("resource-name-env-suffixed", "pass", "resource declarations include environment signal or none found"))
    if secret_hits:
        rules.append(Rule("secret-not-in-source", "fail", f"literal secret-like values found: {', '.join(secret_hits[:5])}"))
    else:
        rules.append(Rule("secret-not-in-source", "pass", "no literal secret-like values found"))
    if default_cred_hits:
        rules.append(Rule("no-default-creds", "fail", f"default credential dependency found: {', '.join(default_cred_hits[:5])}"))
    else:
        rules.append(Rule("no-default-creds", "pass", "no default credential dependency found"))


def secret_disjoint_rule(dev: Path, test: Path, rules: list[Rule]) -> None:
    dev_refs = secret_refs(dev) if dev.exists() else set()
    test_refs = secret_refs(test) if test.exists() else set()
    overlap = dev_refs & test_refs
    if overlap:
        rules.append(Rule("dev-test-secret-disjoint", "fail", f"secret references overlap: {', '.join(sorted(overlap)[:5])}"))
    else:
        rules.append(Rule("dev-test-secret-disjoint", "pass", "dev/test secret references do not overlap"))


def pulumi_secret_disjoint_rule(dev_stack: Path, test_stack: Path, rules: list[Rule]) -> None:
    if not dev_stack.exists() or not test_stack.exists():
        rules.append(Rule("dev-test-secret-disjoint", "fail", "Pulumi dev/test stack files are required for secret comparison"))
        return
    dev_refs = pulumi_stack_secret_refs(dev_stack)
    test_refs = pulumi_stack_secret_refs(test_stack)
    overlap = dev_refs & test_refs
    if overlap:
        rules.append(Rule("dev-test-secret-disjoint", "fail", f"Pulumi secret/config references overlap: {', '.join(sorted(overlap)[:5])}"))
    else:
        rules.append(Rule("dev-test-secret-disjoint", "pass", "Pulumi dev/test secret/config references do not overlap"))


def pulumi_stack_secret_refs(path: Path) -> set[str]:
    refs: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        lowered = line.lower()
        if "secret" in lowered or "password" in lowered or "token" in lowered or "/dev/" in line or "/test/" in line:
            value = line.split(":", 1)[-1].strip().strip('"').strip("'")
            if value:
                refs.add(value)
    return refs


def secret_refs(root: Path) -> set[str]:
    refs: set[str] = set()
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".tf", ".tfvars", ".ts", ".py", ".go", ".cs"}:
            refs.update(SECRET_REF_RE.findall(path.read_text(encoding="utf-8", errors="replace")))
    return refs


def checked_in_state_rule(root: Path, rules: list[Rule]) -> None:
    hits = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.name in {"terraform.tfvars", "pulumi.config.encrypted.yaml"}]
    if hits:
        rules.append(Rule("no-checked-in-tfvars-or-pulumi-secrets", "warn", f"checked-in local config files found: {', '.join(hits)}"))
    else:
        rules.append(Rule("no-checked-in-tfvars-or-pulumi-secrets", "pass", "no checked-in tfvars or Pulumi encrypted config found"))


if __name__ == "__main__":
    sys.exit(main())
