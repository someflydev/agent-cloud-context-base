---
accb_origin: canonical
accb_source_path: context/specs/architecture/base.md
accb_role: architecture
accb_version: 1
---

# Baseline Architecture Constraints

Architecture stays explicit enough that an assistant can identify the changed
cloud boundary, the owning workload, and the correct validation path without
broad scanning. A repo should make clear whether the active boundary belongs to
a function, managed container, Kubernetes API, worker, job, cron workload, or
IaC-only surface.

Architectural truth must make these surfaces concrete:

- Trigger contracts and event shapes.
- Identity bindings between workloads and managed resources.
- Secret bindings and the provider-native secret store.
- Persistence seams and managed-service ownership.
- Network seams, including public, private, and provider-managed ingress.
- IaC dev/test isolation surface: state, names, secret paths, and identities.
- Observability surface: logs, metrics, traces, alarms, and correlation fields.

If a change crosses one of these surfaces, the spec must point to the proof
that exercises it.
