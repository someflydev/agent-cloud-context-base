---
accb_origin: canonical
accb_source_path: context/specs/evolution/base.md
accb_role: evolution
accb_version: 1
---

# Safe Evolution Rules

New features extend the existing spec and validation model instead of bypassing
it. A useful change either preserves the current cloud contract or refines it
with a clearer boundary and stronger proof.

Every meaningful change preserves or refines:

- Trigger contracts.
- Identity bindings.
- IaC dev/test isolation.
- Validation gates.
- Startup order.
- Repo-local operator guidance.

Spec drift is a real defect because it makes future autonomy unsafe. When code,
IaC, startup rules, or validation commands change, the corresponding spec or
validation narrative changes with them.
