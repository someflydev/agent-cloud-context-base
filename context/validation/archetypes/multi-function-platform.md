---
accb_origin: canonical
accb_source_path: context/validation/archetypes/multi-function-platform.md
accb_role: validation
accb_version: 1
---

# Multi Function Platform Validation

Exercise each function with its own trigger fixture, then run one end-to-end
path across the platform boundary. Include the IaC isolation gate for every
function, queue, topic, secret, and persistence resource.

Proof commands should cover per-function trigger tests, a replay test per
dedupe boundary, and a DLQ or redrive proof when eventing exists.

Expected failure modes are mismatched event schemas between functions, shared
identity bindings, missing DLQ alarms, cross-environment state, and duplicate
effects during replay. Reference eventing, replay, identity, and IaC isolation
doctrine for the governing rules.
