# Pub/Sub Dead Letter Pattern

Use one main topic, one subscription, and one dead-letter topic per
environment. Configure retry policy and max delivery attempts.

Producer:

```python
publisher.publish(topic_path, data, dedupe_key=dedupe_key)
```

Consumer:

```python
def callback(message):
    try:
        process(message.data)
        message.ack()
    except RetryableError:
        message.nack()
```

Replay:

```sh
gcloud pubsub subscriptions pull accb-dev-dlq-sub --limit=10 --format=json
gcloud pubsub topics publish accb-dev-main --message="$BODY"
gcloud pubsub subscriptions ack accb-dev-dlq-sub --ack-ids="$ACK_ID"
```

Resource shape:

```hcl
resource "google_pubsub_topic" "dlq" {
  name = "accb-${var.environment}-orders-dlq"
}

resource "google_pubsub_subscription" "main" {
  name  = "accb-${var.environment}-orders-sub"
  topic = google_pubsub_topic.main.name
  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }
  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "300s"
  }
}
```

Consumer contract:

- Ack only after the durable side effect commits.
- Nack retryable errors and let Pub/Sub apply retry policy.
- Do not nack terminal poison messages forever; publish a failure record.
- Use an application `dedupe_key` attribute for idempotency.
- Track delivery attempt when available.

Replay runbook:

1. Create or identify a DLQ subscription for operator reads.
2. Pull a bounded batch and persist it as incident evidence.
3. Validate schema and confirm the failed dependency has recovered.
4. Publish accepted messages back to the main topic.
5. Ack DLQ messages only after republish succeeds.
6. Leave rejected messages in the incident evidence store.
7. Watch subscription backlog and dead-letter metrics.

Operator command:

```sh
gcloud pubsub subscriptions pull "$DLQ_SUB" \
  --limit=10 \
  --format=json > dlq-batch.json
```

Validation checklist:

- Dead-letter topic grants publisher rights to the Pub/Sub service account.
- Main subscription grants subscriber rights only to the runtime identity.
- Replay identity can publish to main and ack DLQ, but not alter topics.
- Logs include `message_id`, `dedupe_key`, `delivery_attempt`, and `trace_id`.
- Dev and test projects or prefixes remain disjoint.
