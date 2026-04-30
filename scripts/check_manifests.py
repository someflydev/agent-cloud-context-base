import glob
import json
import os
import sys

import yaml


REQUIRED_FIELDS = {
    "schema_version",
    "name",
    "description",
    "archetype",
    "primary_stack",
    "secondary_stacks",
    "provider",
    "runtime_tier",
    "primary_language",
    "generated_repo_target",
    "iac_tool",
    "triggers",
    "aliases",
    "scenario_patterns",
    "required_context",
    "optional_context",
    "preferred_examples",
    "recommended_templates",
    "repo_signals",
    "task_hints",
    "warnings",
    "bootstrap_defaults",
    "iac_layout",
    "env_isolation",
    "cloud_integration_test_strategy",
    "cost_band_per_test_run",
    "smoke_test_expectations",
    "prompt_first_support",
}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def stem(path):
    return os.path.splitext(os.path.basename(path))[0]


errors = []
manifest_paths = sorted(glob.glob("manifests/*.yaml"))
manifests = [load_yaml(path) for path in manifest_paths]

with open("context/accb/profile-rules.json", "r", encoding="utf-8") as handle:
    profile_rules = json.load(handle)

scenario_map = load_yaml("context/scenarios/scenario-profile-map.yaml")
scenario_keys = set(scenario_map.get("patterns", {}))
profile_manifest_keys = set(profile_rules.get("manifest_capabilities", {}))
stack_keys = {stem(path) for path in glob.glob("context/stacks/*.md")}
archetype_keys = {stem(path) for path in glob.glob("context/archetypes/*.md")}
workflow_keys = {stem(path) for path in glob.glob("context/workflows/*.md")}

if len(manifest_paths) != 32:
    errors.append(f"expected 32 manifest yaml files, found {len(manifest_paths)}")

for path, manifest in zip(manifest_paths, manifests):
    name = manifest.get("name")
    missing = sorted(REQUIRED_FIELDS - set(manifest))
    if missing:
        errors.append(f"{path}: missing fields {missing}")
    if manifest.get("schema_version") != 2:
        errors.append(f"{path}: schema_version must be 2")
    if name != stem(path):
        errors.append(f"{path}: name {name!r} must match file stem")
    if name not in profile_manifest_keys:
        errors.append(f"{path}: name not in profile-rules manifest_capabilities")
    if manifest.get("archetype") not in archetype_keys:
        errors.append(f"{path}: archetype does not resolve")
    primary_stack = manifest.get("primary_stack")
    if primary_stack != "none" and primary_stack not in stack_keys:
        errors.append(f"{path}: primary_stack {primary_stack!r} does not resolve")
    for scenario in manifest.get("scenario_patterns") or []:
        if scenario not in scenario_keys:
            errors.append(f"{path}: scenario pattern {scenario!r} does not resolve")
    for task_hint in manifest.get("task_hints") or []:
        if task_hint not in workflow_keys:
            errors.append(f"{path}: task_hints entry {task_hint!r} does not resolve")
    iac_layout = manifest.get("iac_layout") or {}
    if iac_layout.get("dev_path") == iac_layout.get("test_path"):
        errors.append(f"{path}: iac dev_path and test_path must differ")
    env = manifest.get("env_isolation") or {}
    if env.get("env_var_prefix_dev") == env.get("env_var_prefix_test"):
        errors.append(f"{path}: env var prefixes must differ")
    if env.get("secret_path_dev") == env.get("secret_path_test"):
        errors.append(f"{path}: secret paths must differ")

extra_profile_keys = profile_manifest_keys - {manifest.get("name") for manifest in manifests}
if extra_profile_keys:
    errors.append(f"profile-rules has manifest keys with no file: {sorted(extra_profile_keys)}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)

print("manifest integrity checks passed")
