# K8s Job Workload

Load this role pack for one-off Kubernetes Jobs. It describes the provider-agnostic invocation, parallelism, timeout, cleanup, identity, and validation shape for finite batch work.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Require a namespace per environment and per tenant when tenancy is in scope.
- Use a namespaced service account mapped through the provider identity-to-pod mechanism.
- Keep Job RBAC separate from API, worker, cronjob, and control-plane roles.
- Use immutable image digests promoted from dev to test.
- Declare whether Jobs are invoked by CI, a controller, a workflow engine, or a human operator.

## Workload Surface

- Kind: Job.
- Invocation: create a new Job per run; do not reuse completed Job objects as mutable state.
- Parallelism: set `parallelism` explicitly.
- Completion: set `completions` explicitly when more than one unit of work exists.
- Retry: set `backoffLimit` based on whether the work is idempotent and retryable.
- Timeout: set `activeDeadlineSeconds` for every Job.
- Cleanup: set `ttlSecondsAfterFinished` unless audit retention requires preserved Job objects.
- Resources: set requests and limits for predictable scheduling and quota enforcement.
- Idempotency: each invocation needs a run id and effect contract.

## Manifests / Charts

- Kustomize layout uses a Job manifest with overlays for dev and test parameters.
- Helm layout templates command, args, resources, timeout, service account, and labels.
- Reference `context/stacks/k8s-kustomize-conventions.md` or `context/stacks/k8s-helm-conventions.md`.
- Parameterize image digest, command, args, run id, parallelism, completions, deadline, and TTL.
- Keep dev and test job names, input paths, output paths, and secret paths separate.
- Add labels for `app.kubernetes.io/name`, `part-of`, `component=job`, `env`, `run-id`, and tenant when applicable.

## Networking

- Jobs usually do not need inbound Services.
- Add egress policy for storage, databases, queues, telemetry, and required external APIs when enforcement exists.
- Keep private endpoint and NAT requirements declared through the selected cluster base.
- Tenant-aware Jobs must read and write tenant-scoped resources.
- Do not allow direct cross-namespace access unless a policy declares the path.

## Identity Binding

- Use one service account for the Job role.
- Reference the provider identity stack through the selected cluster base.
- Grant read and write permissions only for the declared input and output resources.
- Grant queue or event permissions only when the Job is a producer or consumer by contract.
- Do not share the Job identity with API or worker roles.

## Secrets

- Use External Secrets Operator for runtime secret projection.
- Reference `context/stacks/secrets-aws-secrets-manager.md`, `context/stacks/secrets-gcp-secret-manager.md`, or `context/stacks/secrets-azure-key-vault.md` for the selected provider.
- Prefer short-lived provider identity over static credentials.
- Do not place secret values in Helm values, Kustomize generators, or checked-in manifests.
- Keep secret source paths environment-specific.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit logs with run id, shard id, attempt, input, output, outcome, duration, trace id, and tenant where applicable.
- Export completion, failure, retry, duration, and resource metrics.
- Keep Job termination messages useful for failed-run triage.
- Record completed and failed Job evidence in test.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware Jobs.
- Prove a successful Job reaches `Complete`.
- Prove a failing Job respects `backoffLimit` and `activeDeadlineSeconds`.

## Anti-Patterns

- Running finite work as a long-lived Deployment loop.
- Leaving completed Jobs forever without an audit reason.
- Omitting deadlines for external API or database work.
- Sharing input or output locations between dev and test.
