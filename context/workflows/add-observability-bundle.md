# Add Observability Bundle

Use this workflow when adding structured logs, metrics, and traces to a function, managed container, or Kubernetes workload.

## Preconditions

- Workload entry point, provider observability destination, and runtime language are known.
- Trace context source is known for HTTP, event payload, queue message, or job invocation.
- Dev/test configuration, secret paths, and exporter identities are disjoint where applicable.

## Sequence

1. Pick the OpenTelemetry exporter target and provider-native log/metric destination.
2. Define structured log fields: timestamp, severity, service, env, request or event id, correlation id, tenant when present, and outcome.
3. Configure trace context propagation from HTTP headers or trigger metadata.
4. Add custom metrics for the business event or workload effect being changed.
5. Ensure secrets and payloads with sensitive data are redacted before logging.
6. Wire provider or collector configuration through IaC and workload config.
7. Add smoke assertions for log shape and metric emission when local tooling supports it.
8. Add an integration check that one request emits a log, metric, and trace in test.
9. Document the query or dashboard path operators use for the new signal.

## Outputs

- Structured logging, metrics, tracing configuration, runtime instrumentation, and observability verification.

## Validation Gates

- `changed-boundary-proof` from `profile-rules.json`
- `secret-not-in-source`
- `identity-least-privilege-declared`

## Related Docs

- `context/doctrine/observability-cloud-native.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/stacks/observability-otel-cloud.md`

## Common Pitfalls

- Logging full event payloads that may contain secrets or customer data.
- Adding traces without propagating the incoming trace context.
- Treating local console output as proof that cloud observability works.
