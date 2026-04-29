# K8s Worker Workload

Load this role pack for long-running Kubernetes workers that consume queues, streams, or topics. It describes the provider-agnostic Deployment, KEDA scaling, shutdown, idempotency, and validation shape.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Require a namespace per environment and per tenant when tenancy is in scope.
- Use a namespaced service account mapped through the provider identity-to-pod mechanism.
- Keep worker RBAC separate from API, job, cronjob, and control-plane roles.
- Use immutable image digests promoted from dev to test.
- Ensure the cluster base supports KEDA or a documented installation path.

## Workload Surface

- Kind: Deployment plus KEDA ScaledObject for queue-driven scaling.
- Replicas: set `minReplicaCount` explicitly; use zero only when cold-start delay is acceptable.
- Queue targets: support SQS, Pub/Sub, Service Bus, Event Hubs, Kafka, and Redis through KEDA scalers.
- Concurrency: define messages or partitions processed per pod.
- Shutdown: handle SIGTERM, stop fetching new work, finish or checkpoint active work, and release leases.
- Probes: readiness reports consumer health; liveness reports event-loop or process health; startup covers warmup.
- Resources: set requests for steady concurrency and limits for downstream quota protection.
- Disruption: define a PodDisruptionBudget when `minReplicaCount` is greater than one.
- Idempotency: every message handler has a dedupe key, effect checksum, status, and TTL contract.

## Manifests / Charts

- Kustomize layout uses Deployment, ScaledObject, ServiceAccount, and optional PDB resources.
- Helm layout templates worker command, env, resources, KEDA trigger metadata, and identity bindings.
- Reference `context/stacks/k8s-kustomize-conventions.md` or `context/stacks/k8s-helm-conventions.md`.
- Parameterize queue name, scaler type, polling interval, cooldown period, min/max replicas, and image digest.
- Keep dev and test queue names, consumer groups, and release names separate.
- Add labels for `app.kubernetes.io/name`, `part-of`, `component=worker`, `env`, and tenant when applicable.

## Networking

- Workers usually do not need inbound Services.
- Add egress policy for queue endpoints, databases, telemetry, and required external APIs when enforcement exists.
- Keep private endpoint and NAT requirements declared through the selected cluster base.
- Tenant-aware workers must consume tenant-scoped queues or enforce tenant identifiers in the handler contract.
- Do not allow direct cross-namespace access unless a policy declares the path.

## Identity Binding

- Use one service account for the worker role.
- Reference the provider identity stack through the selected cluster base.
- Grant queue receive/delete/ack permissions separately from publish or write permissions.
- Grant DLQ access only when replay or inspection requires it.
- Do not share the worker identity with API or control-plane roles.

## Secrets

- Use External Secrets Operator for runtime secret projection.
- Reference the provider secret store stack added by PROMPT_12.
- Keep queue credentials provider-native where possible and avoid static keys.
- Do not place secret values in Helm values, Kustomize generators, or checked-in manifests.
- Keep secret source paths environment-specific.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit logs with message id, dedupe key, attempt, queue, outcome, latency, trace id, and tenant where applicable.
- Export queue depth, age, handler duration, success, retry, and DLQ metrics.
- Reference `context/stacks/k8s-keda-autoscaling.md` for scaler metrics and cooldown discipline.
- Record drain and retry behavior in test evidence.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware workers.
- Prove queue-driven scale-out and scale-in through KEDA in test.
- Prove idempotency by replaying the same message and observing one effect.

## Anti-Patterns

- Using a web API Deployment as a worker by changing only the command.
- Acknowledging messages before durable effects complete.
- Scaling workers without downstream quota limits.
- Sharing consumer groups, queues, or identities between dev and test.
