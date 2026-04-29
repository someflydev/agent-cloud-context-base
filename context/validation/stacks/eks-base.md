---
accb_origin: canonical
accb_source_path: context/validation/stacks/eks-base.md
accb_role: validation
accb_version: 1
---

# EKS Base Validation

Validate cluster reachability, node readiness, workload readiness, service
routing, and rollback behavior in the selected test lane. Use `kubectl`
commands against the declared context only.

Invariants: workloads have distinct roles, service accounts map to least
privilege IAM roles, namespaces are explicit, resource limits are present, and
event-driven workers have DLQ proof when applicable.

PROMPT_11 adds deeper stack-specific gates.
