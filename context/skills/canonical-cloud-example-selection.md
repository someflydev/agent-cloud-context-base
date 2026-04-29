# Canonical Cloud Example Selection

Use this skill to choose the canonical example for a provider, runtime tier, language, and IaC cell. It resolves ambiguity by filtering `examples/catalog.json`, preferring the most recently verified compatible entry, and rejecting examples that conflict with newer doctrine.

## Procedure

1. Identify provider, runtime tier, language, IaC tool, archetype, and support services before choosing an example.
2. Filter `examples/catalog.json` by provider.
3. Filter the remaining entries by runtime tier.
4. Filter by language and framework where relevant.
5. Filter by IaC tool and provider-specific infrastructure style.
6. Prefer examples whose support services match the active manifest.
7. Prefer the most recently verified entry among otherwise equal candidates.
8. Reject examples that contradict current doctrine for dev/test isolation, secrets, eventing, idempotency, observability, or runtime tier selection.
9. If no verified example exists, say that explicitly and proceed with stack doctrine instead of forcing a bad match.
10. Record the selected example path and why it was chosen.

## Good Triggers

- "which canonical example fits?"
- "pick an example"
- "provider/runtime/language cell"
- "most recently verified example"
- "example contradicts doctrine"
- "no exact example exists"

## Avoid

- loading several examples as a substitute for a decision
- choosing an example from the wrong provider or runtime tier
- using stale example behavior over current doctrine
- ignoring IaC tool mismatch
- presenting an unverified example as canonical without qualification
