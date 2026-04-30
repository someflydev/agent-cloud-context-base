# Add Replay And DLQ Handling

Use this workflow when adding explicit duplicate-delivery protection, DLQ handling, and operator-driven replay for an event-driven workload.

## Preconditions

- Event source, consumer, retry policy, and DLQ destination are known.
- Dedupe store choice and TTL expectations are declared.
- Dev/test eventing resources, dedupe store, identities, and state are disjoint.

## Sequence

1. Declare the dedupe key strategy from provider id, object version, message id, or business key.
2. Author the dedupe store binding in the same environment as the workload.
3. Record accepted, duplicate, failed, and replayed attempts with enough audit metadata.
4. Author the DLQ destination, alarm, and inspect command.
5. Author an operator-driven replay tool or command that re-enters the normal idempotent path.
6. Limit replay batch size and avoid automatic replay loops.
7. Add tests that send the same event twice and assert a single durable effect.
8. Add tests that send a poison message and assert DLQ landing.
9. Add tests that replay from DLQ and assert idempotent recovery.

## Outputs

- Dedupe store binding, DLQ destination, alarm, replay command/tool, and replay integration tests.

## Validation Gates

- `function-idempotency-proof` from `profile-rules.json`
- `eventing-dlq-path`
- `storage-real-roundtrip-in-test-stack`

## Related Docs

- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/stacks/eventing-gcp-pubsub.md`

## Common Pitfalls

- Using process memory as the dedupe store.
- Replaying directly into side effects instead of the normal handler path.
- Letting DLQ alarms exist without an operator inspection path.
