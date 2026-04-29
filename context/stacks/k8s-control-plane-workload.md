# K8s Control Plane Workload

Load this role pack for Kubernetes-native controllers, reconcilers, and administrative services. It describes the provider-agnostic Deployment, leader election, RBAC, resource, and validation shape.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Require a namespace per environment and per tenant when tenancy is in scope.
- Use a namespaced service account mapped through the provider identity-to-pod mechanism.
- Keep control-plane RBAC separate from API, worker, job, and cronjob roles.
- Use immutable image digests promoted from dev to test.
- Declare whether the workload watches namespace-scoped or cluster-scoped resources.

## Workload Surface

- Kind: Deployment.
- Replicas: use two or more replicas only when leader election is implemented.
- Leader election: use Kubernetes Lease objects for singleton reconciliation.
- Probes: readiness reports informer cache sync and dependency readiness; liveness reports process health.
- Resources: set strict requests and limits to prevent a controller from starving tenant workloads.
- Autoscaling: prefer fixed replicas; use HPA only for stateless admission or control-plane APIs with measured metrics.
- Disruption: define a PodDisruptionBudget when multiple replicas are active.
- Rollout: keep maxUnavailable low for reconcilers that protect drift or availability.
- External surface: keep inbound exposure minimal and private by default.

## Manifests / Charts

- Kustomize layout uses Deployment, ServiceAccount, Role or ClusterRole, binding, and optional PDB resources.
- Helm layout templates RBAC, leader-election names, resources, env, probes, and labels.
- Reference `context/stacks/k8s-kustomize-conventions.md` or `context/stacks/k8s-helm-conventions.md`.
- Parameterize image digest, watched namespaces, leader election id, resources, and RBAC scope.
- Keep dev and test leader election ids, namespaces, and release names separate.
- Add labels for `app.kubernetes.io/name`, `part-of`, `component=control-plane`, `env`, and tenant when applicable.

## Networking

- Control-plane workloads should not be internet-exposed by default.
- Use ClusterIP Services only when webhooks, metrics, or internal APIs require them.
- Add NetworkPolicy to restrict inbound access to the API server, ingress controller, or allowed namespaces.
- Add egress policy for Kubernetes API, telemetry, cloud APIs, and required external APIs when enforcement exists.
- Tenant-aware reconcilers must avoid direct cross-tenant access unless policy declares the path.

## Identity Binding

- Use one service account for the control-plane role.
- Reference the provider identity stack through the selected cluster base.
- Grant Kubernetes RBAC with the smallest verbs and resources required.
- Grant cloud API permissions only for declared reconciliation targets.
- Avoid cluster-wide RBAC unless the controller genuinely manages cluster-scoped resources.

## Secrets

- Use External Secrets Operator for runtime secret projection.
- Reference the provider secret store stack added by PROMPT_12.
- Prefer workload identity over static cloud credentials.
- Do not place secret values in Helm values, Kustomize generators, or checked-in manifests.
- Keep secret source paths environment-specific.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit logs with reconcile id, resource kind, namespace, name, generation, outcome, duration, trace id, and tenant where applicable.
- Export reconcile count, error count, queue depth, lease ownership, cache sync, and API throttling metrics.
- Record leader-election transitions during rollout evidence.
- Alert on repeated reconcile errors and lost leadership when the controller is availability-critical.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware controllers.
- Prove leader election by running at least two replicas and deleting the leader pod.
- Prove rollback to a previous immutable image digest.

## Anti-Patterns

- Granting blanket cluster-admin to simplify reconciliation.
- Running a singleton controller without leader election and without documenting why.
- Exposing controller internals publicly.
- Sharing a controller identity with application roles.
