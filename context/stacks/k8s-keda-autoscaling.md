# K8s KEDA Autoscaling

Load this stack when Kubernetes workloads use KEDA for event-driven autoscaling. It defines installation expectations, ScaledObject patterns, scaler metadata, cooldowns, and validation gates.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Install KEDA through Helm, an AKS add-on, or an equivalent managed path declared in IaC.
- Pin KEDA version and CRD versions.
- Keep KEDA operator namespace, service account, and cloud identity separate from app workload identities.
- Keep dev and test scaler targets, queues, topics, streams, and consumer groups separate.
- Confirm the cluster has metrics-server and HPA support because KEDA drives HPA objects.

## Workload Surface

- Worker Deployments are the primary KEDA target in accb.
- API workloads may use KEDA only when scaling from an event metric is more accurate than HPA metrics.
- Jobs and CronJobs do not use ScaledObject unless a specific KEDA ScaledJob contract is selected.
- Set `minReplicaCount` explicitly.
- Set `maxReplicaCount` from downstream quota and cost limits.
- Set polling interval and cooldown period deliberately.
- Use `advanced.restoreToOriginalReplicaCount` only when the repo has a clear reason.
- Align per-pod concurrency with scaler thresholds.
- Keep graceful shutdown behavior compatible with scale-in.

## Manifests / Charts

- Kustomize layout includes ScaledObject resources beside the worker Deployment base.
- Helm layout templates ScaledObject trigger metadata through values files.
- Reference `context/stacks/k8s-kustomize-conventions.md` or `context/stacks/k8s-helm-conventions.md`.
- Use TriggerAuthentication only when the scaler cannot use provider-native workload identity.
- Put scaler metadata that identifies queues, topics, streams, and consumer groups in environment overlays or values.
- Do not put secret values in scaler metadata.
- Render dev and test manifests and validate KEDA CRDs with kubeconform when schemas are available.

## Networking

- KEDA operator needs egress to provider APIs or broker endpoints used by scalers.
- Worker pods need egress to the queue or stream and downstream dependencies.
- Add NetworkPolicy when enforcement exists.
- Keep private endpoint, NAT, and DNS requirements declared through the selected cluster base.
- Tenant-aware workers should scale on tenant-scoped queues or include tenant-safe partitioning.

## Identity Binding

- Prefer provider-native identity for scaler authentication.
- On EKS, use IRSA or Pod Identity for AWS SQS scaler access when supported.
- On GKE, use Workload Identity for Pub/Sub scaler access.
- On AKS, use Workload Identity for Service Bus and Event Hubs scaler access when supported.
- Use TriggerAuthentication with ESO-backed secrets only when static or broker credentials are unavoidable.
- Keep KEDA operator identity separate from worker role identity unless the selected scaler requires otherwise.

## Secrets

- Use External Secrets Operator for scaler credentials that cannot use provider identity.
- Reference the provider secret store stack added by PROMPT_12.
- Keep broker passwords, SAS keys, and connection strings out of Helm values and Kustomize generators.
- Store secret source paths under environment-specific prefixes.
- Rotate scaler credentials without changing application images.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Export ScaledObject readiness, desired replicas, actual replicas, queue depth, lag, and cooldown state.
- Log scaler auth failures and metric retrieval errors.
- Alert when max replicas are pinned while backlog grows.
- Record scale-out and scale-in evidence in test.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware scalers.
- Prove scale-out by increasing SQS, Pub/Sub, Service Bus, Event Hubs, Kafka, or Redis backlog.
- Prove scale-in after cooldown.
- Prove rollback of worker image and scaler config.

## Anti-Patterns

- Setting max replicas higher than downstream quota.
- Scaling from queue depth without a worker idempotency contract.
- Sharing queues, topics, streams, or consumer groups between dev and test.
- Storing connection strings directly in rendered ScaledObject manifests.
