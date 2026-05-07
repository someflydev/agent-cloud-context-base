# EventBridge Archive Replay

Create an archive per environment and replay only a bounded time window.

Producer:

```python
events.put_events(Entries=[{
    "Source": "accb.orders",
    "DetailType": "OrderUpdated",
    "Detail": json.dumps(event),
    "EventBusName": os.environ["EVENT_BUS_NAME"],
}])
```

Consumer:

```python
def handler(event, context):
    for item in event["Records"]:
        process(item)
```

Replay:

```sh
aws events start-replay \
  --replay-name accb-dev-replay-20260507 \
  --event-source-arn "$ARCHIVE_ARN" \
  --event-start-time 2026-05-07T14:00:00Z \
  --event-end-time 2026-05-07T15:00:00Z \
  --destination '{"Arn":"'"$BUS_ARN"'","FilterArns":[]}'
```

Guardrails: require an incident ID, cost estimate, bounded event pattern, and
explicit start/end timestamps before replay.

Resource shape:

```hcl
resource "aws_cloudwatch_event_bus" "this" {
  name = "accb-${var.environment}-events"
}

resource "aws_cloudwatch_event_archive" "this" {
  name             = "accb-${var.environment}-events-archive"
  event_source_arn = aws_cloudwatch_event_bus.this.arn
  retention_days   = 7
}
```

Producer contract:

- Use a stable `Source` per bounded domain.
- Use `DetailType` as a versioned event contract name.
- Put idempotency keys in `Detail`, not only in transport metadata.
- Emit structured logs with EventBridge event ID and correlation ID.
- Keep dev and test buses, archives, rules, and targets disjoint.

Consumer contract:

```python
def consume(detail):
    key = detail["dedupe_key"]
    if already_processed(key):
        return
    apply_change(detail)
    mark_processed(key)
```

Replay runbook:

1. Determine whether the fault was producer, router, target, or consumer side.
2. Build the smallest event pattern that captures only affected events.
3. Pick absolute UTC start and end timestamps.
4. Estimate archive scan and target invocation cost.
5. Disable unsafe targets or make consumers idempotent before replay.
6. Start replay with a unique incident-scoped replay name.
7. Watch target errors, throttles, duplicate suppression, and DLQ depth.
8. Close the incident with replay count and skipped event count.

Operator command:

```sh
aws events start-replay \
  --replay-name "$INCIDENT_REPLAY_NAME" \
  --event-source-arn "$ARCHIVE_ARN" \
  --event-start-time "$START_UTC" \
  --event-end-time "$END_UTC" \
  --destination '{"Arn":"'"$BUS_ARN"'","FilterArns":["'"$RULE_ARN"'"]}'
```

Validation checklist:

- Archive retention is finite and documented.
- Replay IAM role cannot write across environments.
- Every target has retry policy and DLQ where supported.
- Runbooks require incident ID and time-bounded replay scope.
- Dashboards separate published, matched, failed, and replayed events.
