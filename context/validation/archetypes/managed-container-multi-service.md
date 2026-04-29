---
accb_origin: canonical
accb_source_path: context/validation/archetypes/managed-container-multi-service.md
accb_role: validation
accb_version: 1
---

# Managed Container Multi Service Validation

Build every image and prove each service starts with its declared identity,
secrets, and network exposure. Exercise at least one cross-service path and the
public/private boundary when one exists.

Proof commands should include image builds, readiness probes, route smoke
tests, a private reachability denial test where required, and the IaC isolation
gate.

Expected failure modes are missing service-to-service identity, public exposure
of private workers, inconsistent secret paths, unbounded startup ordering, and
dev/test name overlap. Reference networking, identity, container, and IaC
isolation doctrine.
