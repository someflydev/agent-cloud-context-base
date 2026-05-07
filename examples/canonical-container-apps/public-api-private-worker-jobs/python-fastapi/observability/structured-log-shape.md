# Structured Log Shape

Each service and job emits JSON logs with `service`, `env`, `revision`,
`replica`, `request_id`, `trace_id`, `message_id`, `keda_rule`, and
`outcome`. Lane A validates shape through local logs; Lane B validates Azure
Monitor and Container Apps revision correlation.
