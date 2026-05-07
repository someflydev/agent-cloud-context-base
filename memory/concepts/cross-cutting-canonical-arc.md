# Cross-Cutting Canonical Arc

PROMPT_24 extracted common cloud-native patterns into standalone canonical
families:

- `examples/canonical-iac-terraform/` with AWS, GCP, and Azure dev/test
  isolated starters.
- `examples/canonical-iac-pulumi/` with the initial seed set:
  TypeScript/AWS, Python/GCP, Go/AWS, and .NET/Azure.
- `examples/canonical-observability/` for OTel collector and structured-log
  fixtures.
- `examples/canonical-secrets/` for identity-bound secret retrieval.
- `examples/canonical-eventing/` for DLQ, replay, and ordering references.
- `examples/canonical-prompts/` for starter monotonic prompt files.

The initial cross-cutting seed surface is complete. PROMPT_31 owns the deferred
Pulumi provider and language cross-product expansion. PROMPT_32 builds the
cross-provider integration testing harness and arc documentation over this
surface.
