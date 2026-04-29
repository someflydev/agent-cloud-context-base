---
accb_origin: canonical
accb_source_path: context/validation/stacks/aws-lambda-python.md
accb_role: validation
accb_version: 1
---

# AWS Lambda Python Validation

Validate the Python handler with a real AWS event JSON and assert response
shape, status, logs, and side effects. Prefer an ephemeral test stack when
credentials and quota allow it; otherwise use the documented local invocation
lane.

Invariants: dependency packaging is reproducible, handler import succeeds,
environment variables are non-secret references, IAM bindings are least
privilege, and replay with the same event identity is safe.

PROMPT_09 adds deeper stack-specific gates.
