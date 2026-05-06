# Structured Log Shape

Every invocation emits JSON with: `timestamp`, `level`, `msg`, `trace_id`,
`request_id`, `correlation_id`, `provider`, `runtime_tier`, `function_name`,
`dedupe_key`, `decision`, and `latency_ms`.

Decisions are `ALLOW` for a first translated message and `DROP` for duplicate
SQS message IDs.
