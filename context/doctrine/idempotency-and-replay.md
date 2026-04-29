# Idempotency And Replay

Every event-driven cloud workload must be safe to run more than once with the same logical input. Providers retry, users replay, and DLQs re-deliver, so duplicate delivery must not duplicate state.

## Declare The Strategy

- Name the dedupe key before implementing the handler.
- Prefer provider event IDs when they are stable for the trigger.
- Use object version IDs for storage events when overwrite behavior matters.
- Use message IDs for queue and topic delivery when they represent the replay unit.
- Use business keys when provider IDs do not match the effect being protected.

## Store Dedupe State

- Use DynamoDB, Firestore, Cosmos DB, Redis, or another explicit idempotency store.
- Keep the store in the same environment as the workload.
- Scope records by environment and workload role.
- Record enough metadata to audit accepted, duplicate, and failed attempts.
- Avoid process memory as the idempotency source of truth.

## Define TTL Semantics

- Set a TTL that matches the provider retry and replay window.
- Keep TTL long enough for DLQ redrive operations.
- Document when a replay after TTL expiry is allowed to create a new effect.
- Include clock and eventual-consistency assumptions in the strategy.
- Treat indefinite dedupe retention as a conscious storage and privacy choice.

## Prove Replay Safety

- Send the same trigger twice in integration tests.
- Assert exactly one effect at the persistence boundary.
- Assert duplicate delivery returns a safe response.
- Verify duplicate logs and metrics are distinguishable from first processing.
- Test DLQ redrive under the same idempotency contract when a DLQ exists.

## Keep Effects Bounded

- Make external API calls idempotent where the provider supports keys.
- Persist state before acknowledging when the trigger semantics require it.
- Avoid irreversible side effects before dedupe is established.
- Include tenant or account scope in keys for multi-tenant workloads.
- Mark completion `incomplete` when replay behavior is declared but not tested.
