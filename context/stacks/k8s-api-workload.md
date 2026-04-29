# K8s API Workload

Load this role pack for request-serving Kubernetes APIs. It describes the provider-agnostic Deployment, Service, rollout, scaling, and validation shape for an HTTP or gRPC API.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Require a namespace per environment and per tenant when tenancy is in scope.
- Use a namespaced service account mapped through the provider identity-to-pod mechanism.
- Keep API RBAC separate from worker, job, cronjob, and control-plane roles.
- Expose the API through the cluster base ingress story, not a provider-specific shortcut.
- Use immutable image digests promoted from dev to test.

## Workload Surface

- Kind: Deployment plus Service.
- Replicas: start with two replicas in test for rollout and disruption proof; dev may use one.
- Ports: name ports and keep the Service targetPort stable.
- Probes: readiness gates rollout; liveness detects deadlock; startup covers slow initialization.
- Resources: set requests from observed steady state and limits from load-test or quota constraints.
- Autoscaling: use HPA on CPU, memory, or custom RPS/latency metrics.
- Rolling update: set `maxSurge` and `maxUnavailable` explicitly.
- Disruption: define a PodDisruptionBudget for test and production-like environments.
- Lifecycle: use graceful shutdown long enough to drain ingress and in-flight requests.

## Manifests / Charts

- Kustomize layout uses `base/deployment.yaml`, `base/service.yaml`, and overlays for dev and test.
- Helm layout templates Deployment, Service, HPA, PDB, ServiceAccount, and optional Ingress references.
- Reference `context/stacks/k8s-kustomize-conventions.md` or `context/stacks/k8s-helm-conventions.md`.
- Parameterize image repository, image digest, environment, service account, resources, and autoscaling settings.
- Keep dev and test values separate and avoid shared release names.
- Add labels for `app.kubernetes.io/name`, `part-of`, `component=api`, `env`, and tenant when applicable.

## Networking

- The Service should be ClusterIP unless the cluster base explicitly requires another type.
- Ingress or Gateway resources own external reachability.
- Require TLS at the edge for user-facing APIs.
- Add NetworkPolicy to allow ingress only from the ingress controller or allowed namespaces.
- Add egress policy for databases, queues, telemetry, and required external APIs when enforcement exists.
- Tenant-aware APIs must avoid direct cross-namespace calls unless policy declares the path.

## Identity Binding

- Use one service account for the API role.
- Reference the provider identity stack through the selected cluster base.
- Grant only required reads, writes, publishes, and secret access.
- Do not share the API identity with worker or control-plane roles.
- Keep dev and test identity bindings disjoint.

## Secrets

- Use External Secrets Operator for runtime secret projection.
- Reference `context/stacks/secrets-aws-secrets-manager.md`, `context/stacks/secrets-gcp-secret-manager.md`, or `context/stacks/secrets-azure-key-vault.md` for the selected provider.
- Mount secrets as files when rotation without restart matters; use env only for simple non-rotating clients.
- Do not place secret values in Helm values, Kustomize generators, or checked-in manifests.
- Keep secret names stable but source paths environment-specific.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit request logs with route, method, status, latency, request id, trace id, and tenant where applicable.
- Export RED metrics for HPA and SLOs.
- Propagate W3C trace context across downstream calls.
- Record rollout events and readiness failures in test evidence.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware APIs.
- Prove readiness gates rollout by deploying an intentionally unready revision in a controlled test.
- Prove rollback to a previous immutable image digest.

## Anti-Patterns

- Using liveness as a dependency readiness check.
- Exposing the API with a LoadBalancer Service when ingress policy is required.
- Sharing one Deployment for API and worker commands.
- Scaling only by replicas without defining resource requests.
