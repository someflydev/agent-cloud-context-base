# Cross-Cutting Canonical Arc

PROMPT_24 extracted common cloud-native patterns into standalone canonical
families:

- `examples/canonical-iac-terraform/` with AWS, GCP, and Azure dev/test
  isolated starters.
- `examples/canonical-iac-pulumi/` with the full 10-tree Pulumi starter
  surface: TypeScript/AWS/GCP/Azure, Python/AWS/GCP/Azure,
  Go/AWS/GCP/Azure, and .NET/Azure.
- `examples/canonical-observability/` for OTel collector and structured-log
  fixtures.
- `examples/canonical-secrets/` for identity-bound secret retrieval.
- `examples/canonical-eventing/` for DLQ, replay, and ordering references.
- `examples/canonical-prompts/` for starter monotonic prompt files.

The cross-cutting seed surface is complete, including PROMPT_31's deferred
Pulumi provider and language cross-product expansion. PROMPT_32 builds the
parity harness over the now-complete canonical example set.
