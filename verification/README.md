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

## Tier Semantics

`fast` is deterministic: it runs structural validators, a fixed canonical
family coverage set, payload generation, and parity runners. `medium` adds full
example smoke verification and IaC isolation checks. Optional
`local-provider`, `real-cloud`, and `full` lanes update registry entries only
from commands that were actually selected for that lane.

Harness output beginning with `skipped:` records `skipped`, even when the
process exits 0. A `passed` registry result requires the lane command to run
and exit 0 without a skip marker. The top-level `last_verified_*` fields are
derived from tier records and are not proof by themselves.
