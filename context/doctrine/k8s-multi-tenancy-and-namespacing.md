# K8s Multi Tenancy And Namespacing

Multi-tenant Kubernetes workloads require namespace-level isolation by default. Tenant code should not depend on cluster-wide privilege or direct access to another tenant's resources.

## Isolate Tenants

- Use one namespace per tenant.
- Apply ResourceQuota to each tenant namespace.
- Apply LimitRange to each tenant namespace.
- Apply NetworkPolicy to each tenant namespace.
- Keep tenant labels consistent for audit and cleanup.

## Scope Identity

- Use namespaced service accounts for tenant workloads.
- Forbid cluster-wide RBAC for tenant code.
- Bind only the verbs and resources the tenant workload requires.
- Keep image pull credentials per namespace.
- Keep tenant secrets per namespace.

## Control Traffic

- Deny direct cross-namespace traffic by default.
- Use an explicit east-west service when tenants must communicate.
- Prefer mesh policy or shared ingress for controlled cross-tenant paths.
- Log cross-tenant access with tenant identifiers.
- Treat direct service DNS access across namespaces as a policy violation.

## Validate Boundaries

- Test that a tenant cannot read another tenant's secrets.
- Test that NetworkPolicy blocks unintended cross-namespace traffic.
- Test resource limits under load.
- Review RBAC for cluster-scope bindings before completion.
- Mark completion blocked when tenant isolation cannot be proven.
