# Examples

Canonical examples for cloud-native patterns. The machine-readable index is
[`catalog.json`](catalog.json); tiered verification status lives in
[`../verification/example_registry.yaml`](../verification/example_registry.yaml).

## Families

- `canonical-aws-lambda`, `canonical-gcp-functions`, and
  `canonical-azure-functions` cover function-trigger patterns.
- `canonical-cloud-run`, `canonical-app-runner`, and
  `canonical-container-apps` cover managed-container services, workers, jobs,
  sidecars, Dapr, and VPC connector patterns.
- `canonical-eks`, `canonical-gke`, and `canonical-aks` cover multi-role
  Kubernetes platforms.
- `canonical-iac-terraform` and `canonical-iac-pulumi` cover standalone IaC
  starters with dev/test isolation.
- `canonical-eventing`, `canonical-observability`, `canonical-secrets`,
  `canonical-integration-tests`, and `canonical-prompts` cover cross-cutting
  reference patterns.

## Verification

```bash
python3 scripts/verify_examples.py
python3 scripts/verify_examples.py --family canonical-aws-lambda
python3 scripts/run_verification.py --tier fast
```

Local-provider and real-cloud lanes are gated by environment variables because
they can require Docker, emulators, credentials, or billable cloud resources.
