---
accb_origin: canonical
accb_source_path: context/validation/base.md
accb_role: validation
accb_version: 1
---

# Baseline Validation Contract

Every slice identifies the smallest real proof command set for the changed
boundary. Prefer Lane B ephemeral real cloud proof when credentials and cost
controls are available; use Lane A emulator proof only when it still exercises
the same trigger contract and managed-service assumptions.

Minimum expectations:

- A direct changed-boundary proof.
- An IaC isolation proof with `validate_iac_isolation.py` clean.
- A startup or readiness proof when processes or triggers changed.
- An operator-readable failure mode when prerequisites are missing.
- Updated validation notes when the expected proof path changed.

Each plan makes four things visible: command or harness, success condition,
failure condition, and prerequisite or environment assumption that can block.
When any of those are absent, completion cannot be `done`.
