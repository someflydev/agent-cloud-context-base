# Service Bus DLQ Pattern

Azure Service Bus queues include a transfer dead-letter queue. Inspect
`DeadLetterReason` and `DeadLetterErrorDescription` before replay.

Producer:

```csharp
await sender.SendMessageAsync(new ServiceBusMessage(BinaryData.FromObjectAsJson(evt)) {
    MessageId = evt.EventId,
    CorrelationId = evt.CorrelationId
});
```

Consumer:

```csharp
processor.ProcessMessageAsync += async args => {
    await Handle(args.Message);
    await args.CompleteMessageAsync(args.Message);
};
```

Replay:

```sh
az servicebus queue show --resource-group "$RG" --namespace-name "$NS" --name "$QUEUE"
az servicebus queue authorization-rule keys list --resource-group "$RG" --namespace-name "$NS" --queue-name "$QUEUE" --name replay
```

Drain with an operator script that reads from `$QUEUE/$DeadLetterQueue`,
logs reason fields, republishes to `$QUEUE`, and completes the DLQ message.

Resource shape:

```hcl
resource "azurerm_servicebus_queue" "main" {
  name                                    = "accb-${var.environment}-orders"
  namespace_id                            = azurerm_servicebus_namespace.this.id
  max_delivery_count                      = 5
  dead_lettering_on_message_expiration    = true
  requires_duplicate_detection            = true
  duplicate_detection_history_time_window = "PT10M"
}
```

Producer contract:

- Set `MessageId` to the business idempotency key.
- Set `CorrelationId` from the inbound request or workflow.
- Use sessions only when strict per-aggregate ordering is required.
- Send terminal-failure context as application properties.
- Keep dev and test namespaces or queue prefixes disjoint.

Consumer contract:

```csharp
processor.ProcessErrorAsync += args => {
    logger.LogError(args.Exception, "servicebus failure {EntityPath}", args.EntityPath);
    return Task.CompletedTask;
};
```

Replay runbook:

1. Peek DLQ messages and group by `DeadLetterReason`.
2. Reject messages whose schema is no longer supported.
3. Repair payloads only through a reviewed operator transform.
4. Re-send with original correlation ID and a replay marker.
5. Complete the DLQ message after successful send.
6. Abandon on transient replay failure so the operator can retry.
7. Record replayed sequence numbers and lock tokens.

Operator command:

```sh
az servicebus queue show \
  --resource-group "$RG" \
  --namespace-name "$NS" \
  --name "$QUEUE" \
  --query '{count:countDetails.deadLetterMessageCount}'
```

Validation checklist:

- DLQ count and oldest message age are alarmed.
- Replay identity has receive on DLQ and send on main only.
- Consumers log `MessageId`, `CorrelationId`, delivery count, and reason.
- Duplicate detection is enabled when producer retries are expected.
- Auto-forwarding targets do not cross environment boundaries.
