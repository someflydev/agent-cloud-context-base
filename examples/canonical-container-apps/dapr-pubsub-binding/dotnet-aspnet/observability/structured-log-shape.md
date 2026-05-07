# Structured Log Shape

Each app emits JSON logs with `service`, `env`, `revision`, `replica`,
`dapr_app_id`, `trace_id`, `cloudevent_id`, `topic`, `state_key`, and
`outcome`. Lane B also validates Dapr sidecar traces and Azure Monitor
correlation across publisher and subscriber apps.
