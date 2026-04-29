---
accb_origin: canonical
accb_source_path: context/validation/stacks/iac-pulumi-python.md
accb_role: validation
accb_version: 1
---

# Pulumi Python Validation

Validate Pulumi Python with dependency checks, stack selection, preview for dev,
preview for test, and explicit secret handling. The selected stack must match
the intended environment.

Invariants: dev and test use separate stacks, config secrets are marked secret,
resource names include environment, providers are scoped clearly, and
`validate_iac_isolation.py` is clean.

PROMPT_12 adds deeper stack-specific gates.
