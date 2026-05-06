# Structured Log Shape

Every invocation emits JSON with: `timestamp`, `level`, `msg`, `trace_id`,
`request_id`, `correlation_id`, `provider`, `runtime_tier`, `function_name`,
`dedupe_key`, `decision`, and `latency_ms`.

Moderation decisions are `ALLOW`, `FLAG`, or `DROP`. CloudWatch metrics count
each decision by function name, environment, and decision value.
