# Kubernetes Canonical Arc Complete

PROMPT_30 completes the first-class accb Kubernetes example surface with six multi-role platforms:

- `examples/canonical-eks/multi-role-platform/python/` and `examples/canonical-eks/multi-role-platform/go/`
- `examples/canonical-gke/multi-role-platform/python/` and `examples/canonical-gke/multi-role-platform/go/`
- `examples/canonical-aks/multi-role-platform/dotnet/` and `examples/canonical-aks/multi-role-platform/typescript/`

Each platform keeps the PROMPT_23 contract: API, worker, job, cronjob, control-plane IaC, parallel Kustomize and Helm manifests, kind Lane A with provider fakes, ephemeral real-cluster Lane B, replay idempotency coverage, and cron `concurrencyPolicy: Forbid` coverage.

The Go GKE platform includes `keda-autoscaled-workers/` for the promised Pub/Sub backlog autoscaling sub-example. PROMPT_31 completed the Pulumi starter cross-product, and PROMPT_33 completed final parity wiring.
