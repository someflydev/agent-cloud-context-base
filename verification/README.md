# Verification

Verification holds the checks, fixtures, registries, and policy suites for
cloud-native examples and generated repos.

## Main Surfaces

- [`example_registry.yaml`](example_registry.yaml) records tiered status for
  smoke, local-provider, real-cloud, and full verification lanes.
- [`stack_support_matrix.yaml`](stack_support_matrix.yaml) is rendered into
  [`../docs/provider-parity-matrix.md`](../docs/provider-parity-matrix.md).
- `functions/`, `containers/`, `kubernetes/`, `iac/`, and `scenarios/` contain
  parity runners for their respective surfaces.
- `policies/` contains static policy fixtures used by IaC isolation checks.
- `scripts/` contains script-level tests for the base automation.

## Common Commands

```bash
python3 scripts/run_verification.py --tier fast
python3 scripts/run_verification.py --tier medium
python3 scripts/verify_examples.py --family canonical-eks
python3 verification/functions/run_parity_check.py
python3 verification/containers/run_parity_check.py
python3 verification/kubernetes/run_parity_check.py
python3 verification/iac/run_parity_check.py
python3 verification/scenarios/run_scenario_check.py
```

Use `--update-registry` only when intentionally refreshing persisted
verification timestamps.
