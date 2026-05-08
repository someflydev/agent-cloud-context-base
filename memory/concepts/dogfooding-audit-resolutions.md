# Dogfooding Audit Resolutions

PROMPT_32 resolved the PROMPT_24 dogfooding follow-up.

The audit found no accidental divergence requiring repairs. Embedded Terraform
and Pulumi examples continue to match the canonical IaC references for dev/test
state split, stack naming, secret references, and environment-suffixed resource
names. Provider-specialized runtime examples keep their provider-specific
eventing and secret bindings because those differences are legitimate behavior,
not drift from the canonical references.

Resolution:

- Legitimate divergence remains documented by each example README and by the
  canonical family docs.
- Accidental divergence count: zero.
- The new parity runners use `scripts/validate_iac_isolation.py` as the shared
  enforcement point instead of duplicating one-off checks.
- Future changes should treat `examples/canonical-iac-terraform/` and
  `examples/canonical-iac-pulumi/` as the comparison surface for IaC dogfooding.
