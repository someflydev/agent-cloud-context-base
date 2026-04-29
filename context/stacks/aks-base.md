# AKS Base

Load this stack for Azure Kubernetes Service platforms. It owns the AKS cluster boundary, Azure networking integrations, managed identity mapping, and accb Kubernetes validation gates.

## Cluster Surface

- Control plane: pin a supported Kubernetes 1.30 or newer version and record the patch version.
- Node pools: separate system and application pools with autoscaling bounds per environment.
- Capacity: size dev small and test production-like enough to exercise rollout, drain, and autoscaling behavior.
- Networking plugin: use Azure CNI Overlay unless workload routing or legacy constraints require another mode.
- Ingress: use Application Gateway Ingress Controller for Azure-native HTTP ingress or NGINX when portability is more important.
- Identity-to-pod: use Workload Identity for AKS with OIDC issuer and federated credentials.
- Autoscaling: enable cluster autoscaler for node pools; use the KEDA add-on for event-driven workloads.
- Observability add-ons: AKS-managed Prometheus and Grafana are optional but should be declared in IaC when enabled.
- Add-ons: pin metrics-server, CSI drivers, and ingress controller versions represented in IaC.

## Workload Surface

- Compose this base with exactly one role pack per process class.
- APIs use `context/stacks/k8s-api-workload.md`.
- Queue consumers use `context/stacks/k8s-worker-workload.md`.
- One-off batch uses `context/stacks/k8s-job-workload.md`.
- Schedules use `context/stacks/k8s-cronjob-workload.md`.
- Reconcilers and controllers use `context/stacks/k8s-control-plane-workload.md`.
- Keep role-specific Kubernetes service accounts, probes, resources, and scaling rules.
- Use PodDisruptionBudget for workloads that must tolerate node upgrades.
- Use topology spread constraints across zones when regional clusters are enabled.

## Manifests / Charts

- Helm and Kustomize are both first-class in accb.
- Prefer Kustomize for transparent overlays and direct policy validation.
- Prefer Helm for reusable role charts and release packaging.
- Use `context/stacks/k8s-helm-conventions.md` for chart layout.
- Use `context/stacks/k8s-kustomize-conventions.md` for base and overlay layout.
- Keep dev and test namespaces, release names, federated credential subjects, image tags, and secret paths separate.
- Store ACR image digests in generated manifests and promote by digest.

## Networking

- Declare virtual network, subnet, route table, private cluster, and network policy settings in IaC.
- Prefer private clusters for sensitive platforms; document any public API endpoint allowance.
- Use Application Gateway or NGINX ingress with explicit TLS and backend health expectations.
- Add NetworkPolicy for tenant-aware or private workloads.
- Use Azure NAT Gateway or firewall rules for controlled egress.
- For tenant-aware workloads, pair namespaces with ResourceQuota, LimitRange, and NetworkPolicy.

## Identity Binding

- Reference `context/stacks/identity-azure-entra-mi.md` for managed identity and Workload Identity for AKS guidance.
- Create one user-assigned managed identity per workload role unless a manifest justifies sharing.
- Bind Kubernetes service accounts to managed identities with federated credentials scoped by subject.
- Scope Service Bus, Event Hubs, Storage, Cosmos DB, Azure SQL, Key Vault, and ACR access by environment.
- Keep dev and test managed identities, federated credentials, and resource names disjoint.

## Secrets

- Use External Secrets Operator for Kubernetes Secret materialization.
- Reference `context/stacks/secrets-azure-key-vault.md` when PROMPT_12 adds the provider secret stack.
- Store Key Vault names and secret paths under environment-specific naming.
- Do not commit Kubernetes Secret manifests with plaintext data.
- Give each workload role only the secret reads it requires.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit structured logs with cluster, namespace, workload role, pod, container, trace id, and tenant where applicable.
- Export traces, metrics, and logs to Azure Monitor, managed Prometheus, or the selected OpenTelemetry backend.
- Scrape metrics needed for HPA, KEDA, rollout, and SLO checks.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` when namespaces carry tenant boundaries.
- Prove cluster reachability with `kubectl get nodes` and a Ready sample workload.
- Prove rollback by changing an immutable image tag and reverting to a previous digest.

## Anti-Patterns

- Using the node resource group as an application ownership boundary.
- Sharing one managed identity across unrelated workload roles.
- Treating ingress health as pod readiness.
- Rebuilding images during test promotion instead of promoting immutable digests.
