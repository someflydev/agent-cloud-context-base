# Structured Log Shape

Every invocation emits JSON with: `timestamp`, `level`, `msg`, `trace_id`,
`request_id`, `correlation_id`, `provider`, `runtime_tier`, `function_name`,
`dedupe_key`, `decision`, and `latency_ms`.

Decisions are `ALLOW` for the first accepted event and `DROP` for invalid
signatures or duplicate Stripe event IDs.
