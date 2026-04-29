# K8s OTel Collector

Load this stack when Kubernetes workloads need an in-cluster OpenTelemetry Collector. It defines operator-managed collectors, deployment modes, provider exporters, and validation expectations.

## Cluster Surface

- Compose with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Install the OpenTelemetry Operator through Helm or the cluster add-on path selected by the repo.
- Keep collector namespaces, service accounts, and exporter credentials separate for dev and test.
- Use one collector configuration per environment.
- Use node-level collection only when the cluster base and security policy allow the required access.
- Keep provider-specific exporters behind environment values or overlays.

## Workload Surface

- DaemonSet collector: use for node, pod, and host metrics when node access is required.
- Deployment collector: use for application traces, logs, and metrics received through OTLP.
- Sidecar collector: use sparingly for strict per-workload isolation or special routing.
- API workloads send traces and metrics to the Deployment collector.
- Worker, Job, CronJob, and control-plane roles use the same OTLP endpoint unless isolation requires a separate collector.
- Set collector resource requests and limits from telemetry volume, not defaults.
- Use readiness and liveness probes on collectors.
- Use PodDisruptionBudget for collector Deployments that are on the request path.

## Manifests / Charts

- Helm layout keeps collector values in `values.dev.yaml` and `values.test.yaml`.
- Kustomize layout keeps collector manifests in base with environment-specific exporter patches.
- Reference `context/stacks/k8s-helm-conventions.md` or `context/stacks/k8s-kustomize-conventions.md`.
- Configure receivers for OTLP gRPC and HTTP by default.
- Configure processors for memory limiting, batching, resource detection, and attribute filtering.
- Configure exporters per provider and selected backend.
- Keep sensitive exporter config in External Secrets Operator references.

## Networking

- Expose collector receivers as ClusterIP Services.
- Restrict receiver traffic with NetworkPolicy where enforcement exists.
- Allow egress only to provider telemetry endpoints or the selected observability backend.
- Keep node metric collection privileges explicit and reviewed.
- Do not expose OTLP receivers publicly.
- For tenant-aware workloads, include tenant attributes and avoid cross-tenant collector write paths unless approved.

## Identity Binding

- Use a dedicated collector service account.
- Reference `identity-aws-iam.md`, `identity-gcp-iam-sa.md`, or `identity-azure-entra-mi.md` through the cluster base.
- On EKS, grant CloudWatch or AMP permissions through IRSA or Pod Identity.
- On GKE, grant Cloud Trace, Cloud Logging, and Cloud Monitoring permissions through Workload Identity.
- On AKS, grant Azure Monitor or managed Prometheus permissions through Workload Identity for AKS.
- Keep app workload identities separate from collector identities.

## Secrets

- Use External Secrets Operator for exporter tokens, endpoints, and credentials.
- Reference `context/stacks/secrets-aws-secrets-manager.md`, `context/stacks/secrets-gcp-secret-manager.md`, or `context/stacks/secrets-azure-key-vault.md` for the selected provider.
- Prefer provider workload identity over static telemetry keys.
- Do not put exporter tokens in Helm values, Kustomize generators, or checked-in manifests.
- Keep secret source paths environment-specific.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` as the cloud-level observability contract.
- AWS exports target CloudWatch, X-Ray-compatible paths, AMP, or a selected OTLP backend.
- GCP exports target Cloud Trace, Cloud Logging, Cloud Monitoring, or a selected OTLP backend.
- Azure exports target Azure Monitor, managed Prometheus, or a selected OTLP backend.
- Emit collector self-metrics and logs.
- Add resource attributes for service, environment, cluster, namespace, pod, container, workload role, and tenant where applicable.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware telemetry.
- Prove one trace, one metric, and one structured log arrive in the selected backend from test.
- Prove collector rollout and rollback with immutable image digests.
- Prove no plaintext exporter secret appears in rendered manifests.

## Anti-Patterns

- Running one unbounded collector with no resource limits.
- Exposing OTLP receivers outside the cluster.
- Sending tenant data without tenant attributes.
- Giving application pods direct broad telemetry exporter credentials.
