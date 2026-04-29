---
accb_origin: canonical
accb_source_path: context/validation/stacks/aws-lambda-typescript-node.md
accb_role: validation
accb_version: 1
---

# AWS Lambda TypeScript Node Validation

Validate the Node handler with a real AWS event JSON and assert response shape,
status, logs, and side effects. The build output must match the configured
Lambda runtime and handler path.

Invariants: type checks pass, bundling is deterministic, handler startup is
within the runtime budget, IAM bindings are least privilege, and replay with
the same event identity is safe.

PROMPT_09 adds deeper stack-specific gates.
