# Structured Log Shape

Every invocation emits one JSON log object with these fields:

- `timestamp`
- `severity`
- `msg`
- `trace_id`
- `request_id`
- `correlation_id`
- `provider`: `gcp`
- `runtime_tier`: `function`
- `function_name`: `accb-dev-gcp-firebase-onboarding` or matching test name
- `dedupe_key`
- `decision`: `ALLOW` or `DROP`
- `latency_ms`

Lane A minisky captures the same shape locally; Lane B verifies the shape through Cloud Logging for the isolated test deployment.
