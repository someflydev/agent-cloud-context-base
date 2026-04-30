# Add Eventing Seam

Use this workflow when adding a queue, topic, bus, stream, or equivalent event boundary with bounded retry and a dead-letter path.

## Preconditions

- Provider event primitive is chosen for the workload shape.
- Producer, consumer, delivery semantics, and ownership boundary are known.
- Dev/test event resources, DLQ names, identities, and state are disjoint.

## Sequence

1. Pick the primitive using `eventing-seam-selection` and the provider stack conventions.
2. Declare delivery semantics, ordering needs, ack point, visibility or lease timeout, and retry behavior.
3. Author IaC for the primary event resource and separate DLQ destination.
4. Add alarm or metric configuration for nonzero DLQ depth.
5. Grant producer and consumer identities only the required send, receive, ack, and DLQ actions.
6. Wire producer code and consumer handler without hiding provider payload details.
7. Add unit tests for payload construction and consumer parsing.
8. Add integration tests for happy path, retryable failure, poison message, and DLQ landing.
9. Document operator replay commands beside the eventing stack or hand off to the replay workflow.

## Outputs

- Event resource, DLQ, retry policy, alarm, producer wiring, consumer wiring, identity bindings, and tests.

## Validation Gates

- `eventing-dlq-path` from `profile-rules.json`
- `identity-least-privilege-declared`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/stacks/eventing-aws-eventbridge-sqs-sns.md`

## Common Pitfalls

- Adding the primary queue or topic without a DLQ.
- Leaving retry behavior at provider defaults without documenting consequences.
- Publishing events before the durable state change they describe.
