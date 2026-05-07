# Structured Log Shape

Every invocation emits JSON logs with these fields:

- `timestamp`
- `level`
- `msg`
- `trace_id`
- `request_id`
- `correlation_id`
- `provider`: `aws`
- `runtime_tier`: `function`
- `function_name`
- `dedupe_key`: `eventbridge_event_id`
- `decision`: `ALLOW`, `FLAG`, or `DROP` where applicable
- `latency_ms`

The same shape is expected from smoke tests, Lane A ministack runs, and Lane B CloudWatch logs.
