# Event Grid Dead Letter Pattern

Configure each Event Grid subscription with a Storage dead-letter destination.

Producer:

```python
client.send([{
    "id": event_id,
    "subject": "accb/dev/order",
    "eventType": "OrderUpdated",
    "data": payload,
    "dataVersion": "1.0",
}])
```

Consumer:

```python
def main(event):
    process(event.get_json())
```

Replay:

```sh
az storage blob list --container-name eventgrid-dlq --account-name "$ACCOUNT"
az storage blob download --container-name eventgrid-dlq --name "$BLOB" --file event.json --account-name "$ACCOUNT"
az eventgrid event-subscription create --name replay-review --source-resource-id "$TOPIC_ID" --endpoint "$ENDPOINT"
```

Use a Storage queue trigger or runbook to re-publish reviewed events.

Resource shape:

```hcl
resource "azurerm_eventgrid_event_subscription" "this" {
  name  = "accb-${var.environment}-orders"
  scope = azurerm_eventgrid_topic.this.id
  storage_blob_dead_letter_destination {
    storage_account_id          = azurerm_storage_account.dlq.id
    storage_blob_container_name = azurerm_storage_container.dlq.name
  }
}
```

Producer contract:

- Set event ID from a stable business event ID.
- Use subject prefixes that include environment and aggregate type.
- Keep event type names versioned when payload contracts change.
- Include correlation ID and dedupe key in data.
- Publish to environment-scoped custom topics or domains.

Consumer contract:

```python
def handle_event(event):
    payload = event.get_json()
    if seen(payload["dedupe_key"]):
        return
    process(payload)
```

Replay runbook:

1. List blobs written by the Event Grid dead-letter destination.
2. Download a bounded batch for review.
3. Confirm endpoint health and authentication are fixed.
4. Re-publish only accepted events to the source topic.
5. Move replayed blobs to an incident archive prefix.
6. Keep rejected blobs with reason metadata.
7. Watch delivery failures and dead-letter writes during replay.

Operator command:

```sh
az storage blob list \
  --container-name "$DLQ_CONTAINER" \
  --account-name "$ACCOUNT" \
  --prefix "$SUBSCRIPTION_NAME/" \
  --output table
```

Validation checklist:

- Dead-letter container lifecycle is documented.
- Replay publisher cannot write to test from dev or dev from test.
- Event subscription retry policy is explicit.
- Consumer logs include event ID, subject, event type, and correlation ID.
- Storage queue trigger replay is idempotent.
