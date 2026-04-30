# Add K8s Tenant Namespace

Use this workflow when adding a tenant namespace to a Kubernetes multi-tenant platform repo.

## Preconditions

- Tenant identifier, namespace naming convention, and target cluster are known.
- Tenant secret source paths, service accounts, quotas, and network boundaries are declared.
- Dev/test cluster, namespace, state, identity, and secret naming remain disjoint.

## Sequence

1. Declare the tenant namespace name and labels.
2. Add ResourceQuota for compute, storage, object counts, and any platform-specific limits.
3. Add LimitRange defaults for containers.
4. Add default-deny NetworkPolicy and explicit allow policies for required ingress and egress.
5. Add tenant service accounts and workload identity boundaries.
6. Wire tenant secret source paths without copying secret values into manifests.
7. Add Helm values or Kustomize overlay entries according to repo convention.
8. Validate that tenant workloads cannot reach other tenant namespaces or secrets.
9. Run test-cluster apply and smoke a representative tenant workload.

## Outputs

- Tenant namespace manifests, quota, limits, network policies, service accounts, secret path bindings, overlay wiring, and isolation tests.

## Validation Gates

- `k8s-tenant-isolation-evident` from `profile-rules.json`
- `identity-least-privilege-declared`
- `secret-binding-via-identity`

## Related Docs

- `context/doctrine/k8s-multi-tenancy-and-namespacing.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/stacks/k8s-kustomize-conventions.md`

## Common Pitfalls

- Creating a namespace without ResourceQuota or default-deny NetworkPolicy.
- Sharing one service account across tenants.
- Treating naming convention as isolation.
