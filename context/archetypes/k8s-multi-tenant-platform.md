# K8s Multi Tenant Platform

Use this archetype for EKS, GKE, or AKS systems where namespace-per-tenant isolation is part of the product or operating model. It applies when ResourceQuota, LimitRange, NetworkPolicy, namespaced secrets, and tenant-scoped identity are required before application work can be considered complete.

## Common Goals

- Create one namespace per tenant with consistent labels and ownership.
- Apply ResourceQuota and LimitRange to each tenant namespace.
- Deny unintended cross-namespace traffic by default.
- Keep tenant secrets and service accounts namespaced.
- Validate isolation behavior with active test cases.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/k8s-workload-role-separation.md`
- `context/doctrine/k8s-multi-tenancy-and-namespacing.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+k8s+language stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-eks/`, `examples/canonical-gke/`, or `examples/canonical-aks/`

## Common Workflows

- `context/workflows/add-k8s-workload-role.md`
- `context/workflows/add-k8s-tenant-namespace.md`
- `context/workflows/add-helm-or-kustomize-overlay.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/k8s-eks-multi-role-python.yaml`
- `manifests/k8s-gke-multi-role-go.yaml`
- `manifests/k8s-aks-multi-role-typescript.yaml`

## Likely Examples

- `examples/canonical-eks/tenant-namespace-platform/`
- `examples/canonical-gke/tenant-isolated-workers/`
- `examples/canonical-aks/namespaced-review-platform/`

## Typical Anti-Patterns

- Allowing direct cross-namespace access as the normal integration path.
- Sharing one secret across tenants.
- Leaving HPAs unbounded against shared cluster capacity.
- Binding tenant code to cluster-admin or cluster-wide read roles.
- Treating namespace creation as manual operations outside IaC.

## Validation Gates (summary)

- k8s-role-separation-evident: Roles remain separated inside tenant workloads.
- k8s-tenant-isolation-evident: ResourceQuota, LimitRange, and NetworkPolicy exist per tenant namespace.
- secret-binding-via-identity: Tenant secrets are read through namespaced identity and secret bindings.
- identity-least-privilege-declared: Tenant RBAC is namespaced and minimal.
