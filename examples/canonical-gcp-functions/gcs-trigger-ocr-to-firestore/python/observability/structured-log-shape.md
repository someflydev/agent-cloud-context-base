# Structured Log Shape

Every invocation emits one JSON log with:

- `timestamp`
- `severity`
- `msg`
- `trace_id`
- `request_id`
- `correlation_id`
- `provider`
- `runtime_tier`
- `function_name`
- `dedupe_key`
- `decision`
- `latency_ms`

`provider` is `gcp`, `runtime_tier` is `function`, and `decision` is `ALLOW`
for first processing or `DROP` for duplicate object generations.
