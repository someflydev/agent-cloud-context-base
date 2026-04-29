# Observability Cloud Native

Every cloud workload should emit enough telemetry to explain requests, retries, failures, cost drivers, and tenant impact. Logs, metrics, and traces are part of the workload contract and must be declared before the system is called complete.

## Structure Logs

- Emit JSON logs for functions, containers, and Kubernetes workloads.
- Include correlation ID, tenant ID when applicable, trace ID, workload role, and environment.
- Record trigger metadata such as queue name, topic, bucket, route, or job name.
- Log duplicate and replay decisions without exposing secret values.
- Avoid raw request bodies that may contain credentials or personal data.

## Emit Metrics

- Use provider-native metrics for runtime health, latency, errors, concurrency, and throttling.
- Add custom counters for business events such as messages processed or files transformed.
- Track retry, DLQ, dedupe hit, and downstream failure counts.
- Include environment and workload labels.
- Keep metric names stable across dev and test.

## Propagate Traces

- Propagate trace context from trigger payloads where providers supply it.
- Create spans around managed-service calls that are material to the contract.
- Export OpenTelemetry traces to a provider-native backend or declared vendor.
- Use an OTel collector sidecar or daemonset for container and Kubernetes workloads when needed.
- Keep trace sampling explicit for production-shaped examples.

## Protect Sensitive Data

- Do not log secrets.
- Do not log raw PII.
- Do not log full authorization headers, cookies, or connection strings.
- Redact request fields known to carry credentials.
- Verify telemetry output during smoke or integration tests.

## Make Telemetry Testable

- Declare required log fields in the manifest.
- Declare required metrics in the manifest.
- Declare trace export expectations in the manifest.
- Exercise observability in tests, even if assertions start with field presence.
- Mark completion `incomplete` when observability is configured but unverified.
