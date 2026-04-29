# Eventing And DLQ Discipline

Event-driven systems must make delivery, retry, and recovery behavior visible. Every event boundary declares what happens before failure, during retry, and after messages land in a dead-letter path.

## Declare Delivery Semantics

- Treat at-least-once delivery as the default.
- State when FIFO ordering is required and when unordered delivery is acceptable.
- Name the ack point for each handler.
- Set message visibility or lease timeouts longer than normal processing time.
- Keep handler idempotency aligned with the selected delivery model.

## Set Retry Policy

- Declare max attempts for each event source.
- Declare the backoff curve or provider retry profile.
- Keep retries bounded so poison messages reach a recoverable state.
- Avoid infinite automatic replay loops.
- Include duplicate-delivery tests for retryable failures.

## Require DLQ Paths

- Use a separate queue or topic per source as the DLQ destination.
- Alarm when DLQ depth is greater than zero.
- Include source, failure reason, and correlation fields in DLQ messages where the provider allows it.
- Keep DLQ permissions narrower than primary processing permissions.
- Document how operators inspect the DLQ.

## Replay Deliberately

- Make replay operator-driven, not automatic.
- Re-run messages through the same idempotent path as first delivery.
- Limit replay batches to avoid trigger storms.
- Record replay commands beside the eventing stack.
- Stop completion when replay behavior is not defined for an event source.
