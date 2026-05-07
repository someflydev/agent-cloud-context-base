# Event Hubs Checkpoint Recovery

Store checkpoints in an environment-scoped Storage account and Blob container.
On handler failure, leave the checkpoint at the last good offset.

Producer:

```go
producer.SendEventDataBatch(ctx, batch, nil)
```

Consumer:

```go
for partitionClient.ReceiveEvents(ctx, 100, nil) {
  if err := handle(event); err != nil {
    return err
  }
  checkpointStore.SetCheckpoint(ctx, event)
}
```

Replay:

```sh
az eventhubs eventhub consumer-group create --resource-group "$RG" --namespace-name "$NS" --eventhub-name "$HUB" --name replay-incident-123
```

Start the replay consumer from the last known good offset or earliest retained
event, then checkpoint into the replay consumer group only.

Resource shape:

```hcl
resource "azurerm_eventhub" "this" {
  name                = "accb-${var.environment}-events"
  namespace_name      = azurerm_eventhub_namespace.this.name
  resource_group_name = azurerm_resource_group.this.name
  partition_count     = 4
  message_retention   = 3
}
```

Producer contract:

- Choose partition key by aggregate when ordering per aggregate matters.
- Include event ID, sequence, and correlation ID in application properties.
- Keep producer retry bounded and observable.
- Do not use Event Hubs as a durable task queue; retention is finite.
- Keep dev and test namespaces and checkpoint stores disjoint.

Consumer contract:

```go
func handleThenCheckpoint(ctx context.Context, event *azeventhubs.ReceivedEventData) error {
  if err := apply(event); err != nil {
    return err
  }
  return checkpointStore.SetCheckpoint(ctx, event, nil)
}
```

Recovery runbook:

1. Identify the consumer group and partition with the failed checkpoint.
2. Determine last good offset and sequence number from logs.
3. Start a replay consumer group so production checkpoints are untouched.
4. Process from last good offset through the incident end offset.
5. Compare replay side effects against idempotency records.
6. Promote repaired projections only after consistency checks pass.
7. Delete temporary replay consumer groups after retention expires.

Operator command:

```sh
az eventhubs eventhub consumer-group create \
  --resource-group "$RG" \
  --namespace-name "$NS" \
  --eventhub-name "$HUB" \
  --name "$REPLAY_GROUP"
```

Validation checklist:

- Checkpoint container has environment-scoped names.
- Consumer logs include partition ID, offset, sequence, and checkpoint result.
- Replay group names include incident IDs.
- Retention period is long enough for operational recovery.
- Dashboards show lag, processing errors, and checkpoint failures.
