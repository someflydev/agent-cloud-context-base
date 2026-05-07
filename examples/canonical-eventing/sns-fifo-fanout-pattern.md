# SNS FIFO Fanout Pattern

SNS FIFO topics preserve per-message-group ordering while fanning out to SQS
FIFO queues.

Producer:

```ts
await sns.send(new PublishCommand({
  TopicArn: process.env.TOPIC_ARN,
  Message: JSON.stringify(event),
  MessageGroupId: event.accountId,
  MessageDeduplicationId: event.eventId
}));
```

Consumer:

```ts
for (const record of event.Records) {
  await handle(JSON.parse(record.body));
}
```

Operator replay:

```sh
aws sqs receive-message --queue-url "$DLQ_URL" --attribute-names All
aws sns publish --topic-arn "$TOPIC_ARN" --message "$BODY" --message-group-id "$GROUP" --message-deduplication-id "$NEW_ID"
```

Resource shape:

```hcl
resource "aws_sns_topic" "events" {
  name                        = "accb-${var.environment}-orders.fifo"
  fifo_topic                  = true
  content_based_deduplication = false
}

resource "aws_sqs_queue" "subscriber" {
  name       = "accb-${var.environment}-orders-subscriber.fifo"
  fifo_queue = true
}
```

Subscription contract:

- Subscribe only FIFO queues to the FIFO topic.
- Pass the same `MessageGroupId` through the fanout path.
- Use a stable business event ID for `MessageDeduplicationId`.
- Keep subscriber queues independently replayable.
- Use filter policies to reduce fanout noise before it hits consumers.

Consumer side:

```ts
export async function consume(record: SQSRecord) {
  const event = JSON.parse(record.body);
  await idempotency.claim(event.eventId);
  await project(event);
  await idempotency.complete(event.eventId);
}
```

Replay runbook:

1. Identify which subscriber DLQ owns the failed messages.
2. Confirm whether the whole fanout needs replay or only one subscriber.
3. Preserve the original message group when ordering matters.
4. Use a new deduplication ID only when SNS FIFO would suppress the replay.
5. Replay to the topic for fanout-wide repair.
6. Replay directly to one SQS subscriber for subscriber-only repair.
7. Record replay scope and skipped subscribers.

Operator command:

```sh
aws sns publish \
  --topic-arn "$TOPIC_ARN" \
  --message "$BODY" \
  --message-group-id "$GROUP" \
  --message-deduplication-id "$REPLAY_ID"
```

Validation checklist:

- Topic and queues use `.fifo` names.
- Every producer sets group and dedupe IDs explicitly.
- Subscriber DLQs have alarms and separate replay permissions.
- Logs include `message_group_id`, `dedupe_key`, and subscriber name.
- Dev and test topics cannot share subscribers or replay roles.
