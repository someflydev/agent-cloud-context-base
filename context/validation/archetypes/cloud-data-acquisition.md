---
accb_origin: canonical
accb_source_path: context/validation/archetypes/cloud-data-acquisition.md
accb_role: validation
accb_version: 1
---

# Cloud Data Acquisition Validation

Prove ingestion at the real source boundary and persistence at the managed
storage boundary. Validate that retries and partial failures do not duplicate
records.

Proof commands should include a source fixture or controlled pull, one storage
write/read round trip, replay with the same source identity, readiness for any
container worker, and IaC isolation validation.

Expected failure modes are source credentials missing from the provider secret
store, unbounded pagination, duplicate persistence effects, and dev/test
storage overlap. Reference managed service, secret, replay, and IaC isolation
doctrine.
