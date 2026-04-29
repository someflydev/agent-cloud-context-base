---
accb_origin: canonical
accb_source_path: context/validation/stacks/gcp-cloudfn-python.md
accb_role: validation
accb_version: 1
---

# GCP Cloud Functions Python Validation

Validate the function with a real HTTP request or CloudEvent fixture matching
the selected trigger. Prefer a test project or ephemeral deployed function when
credentials and quota allow it.

Invariants: entry point import succeeds, dependency packaging is reproducible,
service account bindings are least privilege, secret access uses Secret
Manager, and replay with the same event identity is safe.

PROMPT_09 adds deeper stack-specific gates.
