# Context Engineering Guide

## How do I keep the assistant from drifting?

Use the router, budget profile, and bundle approval path. Start with one router from `context/router/`, one manifest, and one stack pack. Enable `work.py budget-report` when a generated repo has `budget_report_enabled`.

## How do I prevent silent IaC contamination?

Require manifest `env_isolation` and `iac_layout` declarations, then run `python3 scripts/validate_iac_isolation.py <iac-dir>`. Dev and test must have separate state, env-var prefixes, secret paths, and resource names.

## How do I know which example tiers actually passed?

Read `verification/example_registry.yaml`. It stores tiered metadata under `verification.smoke`, `verification.local_provider`, `verification.real_cloud`, and optional `verification.full`. Refresh the smoke tier with `python3 scripts/run_verification.py --tier medium --update-registry`.

## How do I keep examples honest?

Keep `examples/catalog.json`, `verification/example_registry.yaml`, and the parity runners aligned. A catalog entry says the example exists; the registry says what verification tier ran; parity runners check family-level coverage.

## How do I turn a cloud workload prompt into a concrete repo?

Route through `context/router/scenario-router.md`, select a pattern from `context/scenarios/scenario-profile-map.yaml`, then follow `context/workflows/plan-scenario-derived-repo.md`. The output should name provider, runtime tier, language, IaC tool, manifest, support services, and isolation assumptions.

## How do I ensure derived repos boot the same way?

Generate the `.accb/` payload and read `.accb/SESSION_BOOT.md`. The payload carries profile selection, specs, validation gates, capability coverage, and the scripts needed for `accb_verify` and inspection.

## How do I decide between function, container, and Kubernetes?

Use `context/doctrine/function-vs-container-vs-k8s.md` and the runtime router. Functions fit bounded event handlers; managed containers fit HTTP services, workers, jobs, or heavier runtimes; Kubernetes fits multi-role platforms, tenancy, and cluster-native operational control.

## How do I choose Terraform or Pulumi?

Use `context/router/iac-router.md` and the manifest. Terraform is preferred for declarative module surfaces and broad operator familiarity. Pulumi is preferred when language-native composition or generated components matter. Both must satisfy the same dev/test isolation contract.

## How do I avoid loading too much context?

Load the selected manifest first, then its `required_context`. Add optional context only for the active task. Use one canonical example as the implementation pattern instead of browsing every family.
