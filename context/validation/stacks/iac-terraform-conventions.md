---
accb_origin: canonical
accb_source_path: context/validation/stacks/iac-terraform-conventions.md
accb_role: validation
accb_version: 1
---

# Terraform Conventions Validation

Validate Terraform with formatting, provider initialization, static validation,
and plans for both dev and test. The plan must not hide unintended drift or
environment overlap.

Invariants: backend keys are disjoint, variable files do not contain secrets,
resource names include environment, provider aliases are explicit when needed,
and `validate_iac_isolation.py` is clean.

PROMPT_12 adds deeper stack-specific gates.
