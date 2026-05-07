# SQS DLQ Pattern

Use one main queue and one DLQ per environment. Set `maxReceiveCount` to a
small bounded value, then alert on DLQ depth.

Producer:

```python
import boto3

def publish(queue_url, body, dedupe_key):
    boto3.client("sqs").send_message(
        QueueUrl=queue_url,
        MessageBody=body,
        MessageAttributes={"dedupe_key": {"DataType": "String", "StringValue": dedupe_key}},
    )
```

Consumer:

```python
def handle(record):
    try:
        process(record["body"])
    except RetryableError:
        raise
```

Ordering:

Use FIFO queues for strict ordering. Set `MessageGroupId` to the aggregate ID
and `MessageDeduplicationId` to the idempotency key.

Replay:

```sh
aws sqs receive-message --queue-url "$DLQ_URL" --max-number-of-messages 10
aws sqs send-message --queue-url "$MAIN_URL" --message-body "$BODY"
aws sqs delete-message --queue-url "$DLQ_URL" --receipt-handle "$HANDLE"
```

Resource shape:

```hcl
resource "aws_sqs_queue" "dlq" {
  name = "accb-${var.environment}-orders-dlq"
}

resource "aws_sqs_queue" "main" {
  name                       = "accb-${var.environment}-orders"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 345600
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })
}
```

Consumer contract:

- Treat the message ID as transport metadata, not the business idempotency key.
- Persist `dedupe_key` before side effects when the operation is not naturally idempotent.
- Set visibility timeout above the p95 handler time and below the retry SLO.
- Fail retryable work by returning an error so SQS can redeliver.
- Complete terminal failures only after writing a durable failure record.

Replay runbook:

1. Freeze automated consumers or reduce concurrency to one worker.
2. Capture DLQ depth, oldest message age, and the incident ID.
3. Pull a bounded batch from the DLQ with attributes and message attributes.
4. Inspect payload schema, dedupe key, and failure reason.
5. Re-enqueue only messages that are safe for another processing attempt.
6. Delete from the DLQ only after the main queue send succeeds.
7. Record replayed message IDs in the incident log.
8. Restore normal concurrency after main queue depth and error rate stabilize.

Operator command:

```sh
aws sqs receive-message \
  --queue-url "$DLQ_URL" \
  --max-number-of-messages 10 \
  --message-attribute-names All \
  --attribute-names All > dlq-batch.json
```

Validation checklist:

- Alarm on DLQ visible messages greater than zero.
- Alarm on oldest main queue message age.
- Dashboard processed, retried, failed, and replayed counts by environment.
- Include `correlation_id`, `dedupe_key`, and `receive_count` in logs.
- Keep dev and test queues, DLQs, alarms, and replay roles disjoint.
