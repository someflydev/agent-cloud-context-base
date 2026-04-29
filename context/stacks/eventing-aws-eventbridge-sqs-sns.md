# Eventing AWS EventBridge SQS SNS

Load this stack for AWS eventing in accb-derived repos. It owns EventBridge, SQS, SNS, scheduling, retries, DLQs, replay, and cross-account routing.

## Capability Surface

- Event bus: EventBridge default or custom buses.
- Queue: SQS standard or FIFO.
- Topic: SNS standard or FIFO.
- Scheduler: EventBridge Scheduler.
- Dev names: `<repo>-dev-<event-role>`.
- Test names: `<repo>-test-<event-role>`.
- Dev DLQ names: `<repo>-dev-<source>-dlq`.
- Test DLQ names: `<repo>-test-<source>-dlq`.
- Reference `context/doctrine/eventing-and-dlq-discipline.md`.

## EventBridge Pattern

- Use the default bus for account-local platform events.
- Use custom buses for application domains.
- Define event schemas and required detail fields.
- Add rules with exact source and detail-type filters.
- Use archives when replay is a supported operation.
- Keep archive retention explicit.
- Use Scheduler for delayed and cron-like invocations.

## SQS Pattern

- Use standard queues unless FIFO ordering is required.
- Use FIFO queues when ordering and dedupe are part of the contract.
- Set visibility timeout above normal handler duration.
- Configure redrive policy to a source-specific DLQ.
- Enable server-side encryption.
- Add queue policies only for named publishers.
- Use message attributes for correlation IDs and trace context.

## SNS Pattern

- Use standard topics for fanout without strict ordering.
- Use FIFO topics when subscribers require ordered delivery.
- Configure subscription filter policies.
- Attach DLQs to subscriptions when supported.
- Keep topic policies narrow.
- Use message attributes for tenant, correlation, and trace fields.

## Identity Binding

- Publishers get only publish or put-events permissions.
- Consumers get receive, delete, and visibility permissions only for their queues.
- Replay operators get archive and replay permissions separately.
- KMS permissions are scoped to event resources.
- Reference `context/stacks/identity-aws-iam.md`.

## Replay

- EventBridge replay uses archive and replay names with environment suffixes.
- SQS replay is operator-driven from DLQ to source or a quarantine processor.
- SNS replay requires source retention or subscriber DLQ handling.
- Limit replay batch size.
- Re-run through idempotent handlers.

## CLI Surface

```bash
aws events list-rules --event-bus-name <bus>
aws sqs get-queue-attributes --queue-url <url> --attribute-names RedrivePolicy
aws sns list-subscriptions-by-topic --topic-arn <arn>
```

## Observability

- Alarm on DLQ depth greater than zero.
- Track age of oldest message.
- Track publish failures and throttles.
- Include source, detail type, message ID, and correlation ID in logs.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates

- Every retrying source has a DLQ.
- Replay path is documented.
- FIFO use is deliberate.
- Dev and test event resources differ.
- Permissions separate publish, consume, and replay.

## Anti-Patterns

- Infinite retry loops.
- Shared DLQ for unrelated sources.
- Wildcard event bus policies.
- Acknowledging work before durable effects.
- Automatic replay without operator control.
