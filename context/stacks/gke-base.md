# GKE Base

Load this stack for Google Kubernetes Engine platforms. It owns the GKE cluster boundary, Autopilot or Standard mode decision, Google networking integrations, and accb Kubernetes validation gates.

## Cluster Surface

- Control plane: pin a supported regular or stable channel version and record the effective version.
- Mode: prefer GKE Autopilot unless node-level controls, privileged DaemonSets, GPUs, or custom networking require Standard.
- Standard node pools: separate system and application pools and set autoscaling bounds per environment.
- Networking plugin: use GKE Dataplane V2 for network policy and observability when available.
- Ingress: use GKE Gateway controller for HTTP routing; use Multi Cluster Ingress only when multi-cluster is required.
- DNS: use Cloud DNS for managed zones and in-cluster service discovery integrations.
- Identity-to-pod: use GKE Workload Identity with Kubernetes service accounts mapped to Google service accounts.
- Optional mesh: use Anthos Service Mesh only when policy, mTLS, or traffic management needs justify it.
- Add-ons: pin metrics-server, Gateway API, and any policy controller versions represented in IaC.

## Workload Surface

- Compose this base with exactly one role pack per process class.
- APIs use `context/stacks/k8s-api-workload.md`.
- Queue consumers use `context/stacks/k8s-worker-workload.md`.
- One-off batch uses `context/stacks/k8s-job-workload.md`.
- Schedules use `context/stacks/k8s-cronjob-workload.md`.
- Reconcilers and controllers use `context/stacks/k8s-control-plane-workload.md`.
- In Autopilot, set realistic resource requests because they influence scheduling and cost directly.
- Use PodDisruptionBudget for workloads that need rollout or node maintenance continuity.
- Use topology spread constraints across zones for APIs and control-plane roles.

## Manifests / Charts

- Helm and Kustomize are both first-class in accb.
- Prefer Kustomize for readable overlays and direct `kubectl diff` workflows.
- Prefer Helm for reusable role templates and release packaging.
- Use `context/stacks/k8s-helm-conventions.md` for chart layout.
- Use `context/stacks/k8s-kustomize-conventions.md` for base and overlay layout.
- Keep dev and test namespaces, release names, Workload Identity bindings, image tags, and secret paths separate.
- Store image digests from Artifact Registry in the generated manifest.

## Networking

- Declare VPC-native cluster settings, secondary ranges, private control-plane access, and authorized networks in IaC.
- Prefer private nodes for Standard clusters unless public nodes are explicitly justified.
- Use Gateway API routes for user-facing HTTP and internal Services for east-west calls.
- Add NetworkPolicy with Dataplane V2 for tenant-aware or private workloads.
- Use Cloud NAT or private service connectivity for controlled egress.
- For tenant-aware workloads, pair namespaces with ResourceQuota, LimitRange, and NetworkPolicy.

## Identity Binding

- Reference `context/stacks/identity-gcp-iam-sa.md` for Workload Identity guidance.
- Create one Google service account per workload role unless a manifest justifies sharing.
- Bind Kubernetes service accounts to Google service accounts by namespace and role.
- Scope Pub/Sub, Secret Manager, Cloud SQL, GCS, Firestore, and Artifact Registry permissions by environment.
- Keep dev and test service accounts, IAM bindings, and resource names disjoint.

## Secrets

- Use External Secrets Operator for Kubernetes Secret materialization.
- Reference `context/stacks/secrets-gcp-secret-manager.md` when PROMPT_12 adds the provider secret stack.
- Store secret source names under environment-specific naming or labels.
- Do not commit Kubernetes Secret manifests with plaintext data.
- Give each workload role only the secret reads it requires.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit structured logs with cluster, namespace, workload role, pod, container, trace id, and tenant where applicable.
- Export traces, metrics, and logs to Cloud Trace, Cloud Logging, Cloud Monitoring, or the selected OpenTelemetry backend.
- Scrape metrics needed for HPA, KEDA, rollout, and SLO checks.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` when namespaces carry tenant boundaries.
- Prove cluster reachability with `kubectl get nodes` for Standard or an Autopilot workload readiness check.
- Prove rollback by changing an immutable image tag and reverting to a previous digest.

## Anti-Patterns

- Choosing Standard mode only out of habit.
- Granting broad project roles to a shared node or workload service account.
- Treating Gateway routing success as readiness.
- Rebuilding images during test promotion instead of promoting immutable digests.
