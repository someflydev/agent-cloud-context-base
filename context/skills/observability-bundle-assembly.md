# Observability Bundle Assembly

Use this skill to assemble the smallest useful observability bundle for a cloud workload. It resolves ambiguity by choosing trace context, structured logs, custom metrics, and the provider exporter target without turning observability into an oversized platform project.

## Procedure

1. Identify the workload entry points and async boundaries that create or propagate trace context.
2. Declare the trace context source: HTTP headers, cloud event metadata, queue attributes, scheduler metadata, or generated correlation id.
3. Define the structured-log shape with service, environment, provider, runtime tier, request id, correlation id, tenant when present, and outcome.
4. Define business metrics such as accepted events, processed events, failed events, DLQ depth, replay count, latency, and external API failures.
5. Choose the OpenTelemetry exporter target for the provider: CloudWatch and X-Ray, Cloud Operations, or Azure Monitor.
6. Keep logs, traces, and metrics aligned around the same correlation fields.
7. Add alarms for DLQ depth, error rate, latency, and missing scheduled runs when relevant.
8. Include test or smoke assertions that telemetry configuration loads and redacts secrets.
9. Stop if the bundle cannot explain how an operator follows one request or event across boundaries.

## Good Triggers

- "add observability"
- "structured logs"
- "OTel exporter"
- "trace context"
- "business metrics"
- "three pillars"

## Avoid

- adding telemetry libraries without a correlation model
- logging raw secrets, tokens, or payloads with sensitive fields
- defining infrastructure metrics only while ignoring business events
- sending traces to a provider target unrelated to the selected stack
- treating observability as complete without alarms for recovery paths
