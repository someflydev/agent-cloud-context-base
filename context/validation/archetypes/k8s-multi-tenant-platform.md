---
accb_origin: canonical
accb_source_path: context/validation/archetypes/k8s-multi-tenant-platform.md
accb_role: validation
accb_version: 1
---

# Kubernetes Multi Tenant Platform Validation

Validate role separation and tenant isolation together. Each tenant namespace
must carry its own quota, limits, network policy, identities, and secret paths.

Proof commands should include namespace inspection, quota and limit checks,
network denial across tenants, one allowed in-tenant path, workload readiness,
and the IaC isolation gate.

Expected failure modes are shared service accounts, missing NetworkPolicy,
default namespace deployments, shared secrets, and tenant resources without
quotas. Reference tenancy, identity, networking, and IaC isolation doctrine.
