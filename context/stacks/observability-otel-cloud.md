# Observability OpenTelemetry Cloud

Load this stack for cross-provider observability in accb-derived repos. It owns OpenTelemetry instrumentation, collector deployment patterns, provider exporters, correlation propagation, structured log fields, and validation.

## Capability Surface

- Instrumentation: OpenTelemetry SDKs.
- Collection: direct export or OTel Collector.
- AWS targets: CloudWatch and X-Ray.
- GCP targets: Cloud Logging, Cloud Monitoring, and Cloud Trace.
- Azure targets: Azure Monitor and Application Insights.
- Dev names: `<repo>-dev-<telemetry-role>`.
- Test names: `<repo>-test-<telemetry-role>`.
- Reference `context/doctrine/observability-cloud-native.md`.

## Required Log Fields

- `timestamp`
- `level`
- `msg`
- `service`
- `env`
- `trace_id`
- `span_id`
- `tenant_id`
- `request_id`
- `correlation_id`
- `workload_role`
- `outcome`

## Instrumentation Pattern

- Use provider runtime auto-instrumentation when it is stable for the language.
- Add manual spans around managed-service calls that define the workload contract.
- Propagate W3C `traceparent` where possible.
- Preserve provider trace headers when they are present.
- Emit structured JSON logs.
- Keep metric names stable across dev and test.
- Do not log secrets, raw credentials, or full authorization headers.

## Collector Patterns

- Use a sidecar for single-service container workloads that need local batching.
- Use a daemonset for Kubernetes node-local collection.
- Use a gateway deployment for Kubernetes cluster-level fan-in.
- Use direct export for simple functions when a collector is unnecessary.
- Configure memory limits, batch processors, and retry processors.
- Keep collector config environment-specific.

## AWS Export

- Export traces to X-Ray when AWS-native tracing is selected.
- Export logs and metrics to CloudWatch.
- Use ADOT collector distributions when Kubernetes or ECS support needs them.
- Include AWS request IDs in logs.
- Keep IAM permissions scoped to telemetry writes.

## GCP Export

- Export traces to Cloud Trace.
- Export metrics to Cloud Monitoring.
- Export logs to Cloud Logging through structured stdout or collector exporters.
- Include `logging.googleapis.com/trace` when available.
- Bind telemetry writes to workload service accounts.

## Azure Export

- Export telemetry to Azure Monitor or Application Insights.
- Use managed identity where exporter authentication supports it.
- Include operation ID and request ID correlation.
- Keep connection strings in Key Vault or managed configuration references.
- Scope monitoring roles narrowly.

## CLI Surface

```bash
otelcol --config otelcol.yaml
aws logs describe-log-groups --log-group-name-prefix <repo>-dev
gcloud logging read 'resource.labels.service_name="<service>"'
az monitor app-insights component show --app <name> --resource-group <rg>
```

## Validation Gates

- Required log fields are declared in manifests.
- Trace propagation is tested for request or event paths.
- DLQ, retry, and downstream failure metrics exist when eventing is active.
- Dev and test telemetry resources differ.
- Sensitive data redaction is verified in smoke or integration output.

## Anti-Patterns

- Plain text logs for cloud workloads.
- Traces enabled without propagation.
- Metrics with changing names per environment.
- Collector with no memory or retry limits.
- Logging request bodies that may contain credentials or personal data.
