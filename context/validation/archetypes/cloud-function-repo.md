---
accb_origin: canonical
accb_source_path: context/validation/archetypes/cloud-function-repo.md
accb_role: validation
accb_version: 1
---

# Cloud Function Repo Validation

Run the function trigger proof for the selected provider and language, using a
real event fixture or the provider emulator documented by the stack pack. Run
the IaC isolation gate for the function resources before any cloud deploy.

Expected proof commands are the stack-specific handler or emulator test, an
idempotency replay using the same event identity, and
`python3 scripts/validate_iac_isolation.py <iac dir>` once the generated repo
contains that script.

Common failure modes are malformed trigger fixtures, missing workload identity,
shared dev/test names, absent secret bindings, and replay tests that create a
second side effect. Reference the trigger, replay, identity, secret, and IaC
isolation doctrine instead of duplicating it here.
