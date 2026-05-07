# Pub/Sub Ordering Keys

Enable message ordering on the topic and publisher. Use a stable aggregate ID
as the ordering key.

Producer:

```ts
await topic.publishMessage({
  data: Buffer.from(JSON.stringify(event)),
  orderingKey: event.accountId,
  attributes: { dedupe_key: event.eventId }
});
```

Consumer:

```ts
subscription.on("message", async message => {
  await handle(JSON.parse(message.data.toString()));
  message.ack();
});
```

Replay:

```sh
gcloud pubsub topics publish accb-dev-main --message="$BODY" --attribute=dedupe_key="$NEW_ID" --ordering-key="$ACCOUNT_ID"
```

Resource shape:

```hcl
resource "google_pubsub_topic" "ordered" {
  name = "accb-${var.environment}-ordered-events"
}

resource "google_pubsub_subscription" "ordered" {
  name                       = "accb-${var.environment}-ordered-events-sub"
  topic                      = google_pubsub_topic.ordered.name
  enable_message_ordering    = true
  ack_deadline_seconds       = 30
}
```

Producer contract:

- Enable ordering on the publisher client before sending ordered messages.
- Use a stable aggregate ID as the ordering key.
- Do not mix unrelated aggregates under one hot key.
- Resume publishing for an ordering key after a publish failure is handled.
- Include a dedupe key because ordering does not provide exactly-once effects.

Consumer contract:

```ts
async function consume(message: Message) {
  const event = JSON.parse(message.data.toString());
  await applyInOrder(event.ordering_key, event.sequence);
  message.ack();
}
```

Replay runbook:

1. Identify the affected ordering key or bounded key set.
2. Stop producers for those keys if replay must preserve strict order.
3. Replay from the earliest missing sequence.
4. Use the original ordering key and a replay-specific dedupe key.
5. Verify consumers reject stale sequence numbers.
6. Resume producers after the replay catches up.

Operator command:

```sh
gcloud pubsub topics publish "$TOPIC" \
  --message="$BODY" \
  --attribute=dedupe_key="$REPLAY_DEDUPE_KEY" \
  --ordering-key="$ORDERING_KEY"
```

Validation checklist:

- Ordering is enabled on topic publishers and subscriptions.
- Consumers persist last-applied sequence by ordering key.
- Hot-key metrics are reviewed before choosing ordering keys.
- Replay procedures describe producer pause and resume conditions.
- Dev and test keys use separate topics and subscriptions.
