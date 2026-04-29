# Dogfooding Cloud Arc

New cloud arcs must reuse the base's own artifacts. If a generated example needs a pattern the base already claims to provide, the canonical artifact is the source of truth.

## Reuse Canonical IaC

- Use `examples/canonical-iac-terraform/` for Terraform-shaped examples.
- Use the matching `examples/canonical-iac-pulumi-*` pattern for Pulumi examples.
- Do not invent a parallel IaC layout for a new function or container example.
- Fix the canonical IaC artifact when the current shape is insufficient.
- Keep dev/test isolation identical to the canonical pattern unless a manifest deviation explains it.

## Reuse Secrets And Eventing

- Use `examples/canonical-secrets/` for secret bindings.
- Use `examples/canonical-eventing/` for queues, topics, retries, and DLQs.
- Keep replay and idempotency behavior aligned with the canonical eventing pattern.
- Keep secret paths environment-specific.
- Do not place one-off secret wiring inside an example when the canonical binding applies.

## Treat Drift As Signal

- Treat repeated local workaround as missing base capability.
- Update doctrine, stacks, manifests, or examples before branching the pattern.
- Keep prompt output aligned with current canonical artifacts.
- Add validation when a new invariant becomes important.
- Do not let generated repos become the only documentation of a base rule.

## Verify The Arc

- Run base validation after changing canonical artifacts.
- Run example-specific verification when an example changes.
- Keep catalog and registry metadata aligned with example additions.
- Record dogfooding decisions in memory at prompt boundaries.
- Stop when a needed canonical artifact does not exist yet.
