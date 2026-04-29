---
accb_origin: canonical
accb_source_path: context/validation/archetypes/cloud-multi-provider-experiment.md
accb_role: validation
accb_version: 1
---

# Cloud Multi Provider Experiment Validation

Validate each provider implementation through its own native gates, then compare
the product-visible behavior across providers. Do not treat one provider's
success as proof for another.

Proof commands should include provider-specific trigger or readiness checks,
provider-specific IaC isolation checks, and a comparative parity matrix for the
selected behavior.

Expected failure modes are blended provider assumptions, inconsistent trigger
semantics, shared naming across providers, and comparison results without
equivalent validation depth. Reference runtime selection, cost, identity, and
IaC isolation doctrine.
