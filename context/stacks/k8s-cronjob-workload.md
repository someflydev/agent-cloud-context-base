# K8s CronJob Workload

Load this role pack for scheduled Kubernetes work. It describes the provider-agnostic CronJob shape, concurrency policy, history retention, identity, and validation contract.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Require a namespace per environment and per tenant when tenancy is in scope.
- Use a namespaced service account mapped through the provider identity-to-pod mechanism.
- Keep CronJob RBAC separate from API, worker, job, and control-plane roles.
- Use immutable image digests promoted from dev to test.
- Declare timezone expectations in the schedule owner documentation; Kubernetes schedules are evaluated by the controller.

## Workload Surface

- Kind: CronJob.
- Schedule: make the cron expression explicit in values or overlays.
- Concurrency: default to `concurrencyPolicy: Forbid`.
- Deadline: set `startingDeadlineSeconds` for missed schedules.
- Retry: set the Job template `backoffLimit`.
- Timeout: set the Job template `activeDeadlineSeconds`.
- Cleanup: set `successfulJobsHistoryLimit` and `failedJobsHistoryLimit`.
- Resources: set requests and limits for predictable scheduling and quota enforcement.
- Idempotency: each run needs a schedule timestamp or run id and effect contract.

## Manifests / Charts

- Kustomize layout uses a CronJob manifest with overlays for dev and test parameters.
- Helm layout templates schedule, command, args, resources, service account, history limits, and labels.
- Reference `context/stacks/k8s-kustomize-conventions.md` or `context/stacks/k8s-helm-conventions.md`.
- Parameterize image digest, command, args, schedule, deadline, history, timezone notes, and resource settings.
- Keep dev and test job names, input paths, output paths, and secret paths separate.
- Add labels for `app.kubernetes.io/name`, `part-of`, `component=cronjob`, `env`, and tenant when applicable.

## Networking

- CronJobs usually do not need inbound Services.
- Add egress policy for storage, databases, queues, telemetry, and required external APIs when enforcement exists.
- Keep private endpoint and NAT requirements declared through the selected cluster base.
- Tenant-aware CronJobs must read and write tenant-scoped resources.
- Do not allow direct cross-namespace access unless a policy declares the path.

## Identity Binding

- Use one service account for the CronJob role.
- Reference the provider identity stack through the selected cluster base.
- Grant read and write permissions only for the declared schedule contract.
- Grant publish or queue permissions only when the schedule emits work by contract.
- Do not share the CronJob identity with API or worker roles.

## Secrets

- Use External Secrets Operator for runtime secret projection.
- Reference `context/stacks/secrets-aws-secrets-manager.md`, `context/stacks/secrets-gcp-secret-manager.md`, or `context/stacks/secrets-azure-key-vault.md` for the selected provider.
- Prefer provider identity over static credentials.
- Do not place secret values in Helm values, Kustomize generators, or checked-in manifests.
- Keep secret source paths environment-specific.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit logs with schedule, run id, attempt, input, output, outcome, duration, trace id, and tenant where applicable.
- Export scheduled, missed, successful, failed, retry, and duration metrics.
- Keep termination messages useful for failed-run triage.
- Record at least one manual trigger or controlled schedule proof in test.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware CronJobs.
- Prove the generated Job reaches `Complete`.
- Prove concurrency behavior by confirming overlapping runs are blocked when `Forbid` is selected.

## Anti-Patterns

- Running schedules inside an API process.
- Allowing concurrent runs without an idempotency proof.
- Omitting history limits.
- Sharing input or output locations between dev and test.
