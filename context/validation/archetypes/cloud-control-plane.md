---
accb_origin: canonical
accb_source_path: context/validation/archetypes/cloud-control-plane.md
accb_role: validation
accb_version: 1
---

# Cloud Control Plane Validation

Prove that the control-plane API or function changes real managed state only
through declared identities and audited commands. Include authorization and
idempotency checks for each state-changing action.

Proof commands should include route or trigger smoke tests, an authorized state
change, a denied unauthorized action, replay of one mutating request, and IaC
isolation validation.

Expected failure modes are overbroad identities, missing audit logs, state
changes without dedupe keys, and control actions that span dev/test resources.
Reference identity, replay, observability, and IaC isolation doctrine.
