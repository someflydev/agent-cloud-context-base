---
accb_origin: canonical
accb_source_path: context/validation/stacks/cloudrun-python-fastapi.md
accb_role: validation
accb_version: 1
---

# Cloud Run Python Fastapi Validation

Validate the FastAPI service by building the container, starting it with the
declared environment, exercising health and readiness, and calling one
representative route.

Invariants: the image runs as non-root, listens on the provider port, shuts
down cleanly, reads secrets through provider bindings, and exposes logs with
correlation fields.

PROMPT_10 adds deeper stack-specific gates.
