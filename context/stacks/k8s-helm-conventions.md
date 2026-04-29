# K8s Helm Conventions

Load this stack when a generated Kubernetes repo uses Helm as the first-class manifest package. It defines chart shape, environment values, secret references, image resolution, and validation expectations.

## Cluster Surface

- Compose Helm charts with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Keep chart defaults provider-neutral unless a selected cluster base requires provider-specific resources.
- Use one release per workload role or a clearly named umbrella chart with role subcharts.
- Keep release names, namespaces, values files, and image digests separate for dev and test.
- Use Helm only for rendered Kubernetes objects; cloud resources stay in Terraform or Pulumi.

## Workload Surface

- Each role chart declares its Kubernetes kind explicitly.
- API charts template Deployment, Service, HPA, PDB, ServiceAccount, and optional ingress references.
- Worker charts template Deployment, KEDA ScaledObject, ServiceAccount, and optional PDB.
- Job charts template Job with parallelism, completions, deadline, backoff, and TTL.
- CronJob charts template schedule, concurrencyPolicy, deadlines, and history limits.
- Control-plane charts template Deployment, leader election settings, RBAC, and optional webhook Service.
- All charts set probes, resources, labels, and securityContext by default.

## Manifests / Charts

- Required files: `Chart.yaml`, `values.yaml`, `values.dev.yaml`, `values.test.yaml`, `templates/`, and `tests/` when helm tests are useful.
- `Chart.yaml` includes apiVersion v2, name, description, type, version, and appVersion.
- `values.yaml` contains safe provider-neutral defaults only.
- `values.dev.yaml` and `values.test.yaml` carry environment-specific namespace, image digest, resources, scaling, and secret source references.
- Resolve images by repository plus immutable digest in test.
- Use `app.kubernetes.io/*` labels consistently.
- Keep helper templates small and obvious.

## Networking

- Template Services as ClusterIP unless a role pack and cluster base say otherwise.
- Template Ingress, HTTPRoute, or provider ingress annotations only behind explicit values.
- Put TLS hostnames and certificate references in environment values.
- Keep NetworkPolicy templates available for tenant-aware or private workloads.
- Avoid provider ingress annotations in shared defaults when they only apply to one cluster base.

## Identity Binding

- Template ServiceAccount names per role and environment.
- Put provider identity annotations behind selected cluster-base values.
- Reference `identity-aws-iam.md`, `identity-gcp-iam-sa.md`, or `identity-azure-entra-mi.md` through the cluster base.
- Do not template broad RBAC by default.
- Keep Role, ClusterRole, and binding templates scoped to the role pack contract.

## Secrets

- Use External Secrets Operator for secret injection.
- Reference the provider secret store stack added by PROMPT_12.
- Template ExternalSecret resources with environment-specific remote refs.
- Do not put secret values in any values file.
- Use `helm diff` or rendered manifest review to confirm no secret literals are emitted.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Template annotations, env, ports, and ServiceMonitor or PodMonitor only when the selected observability path supports them.
- Include labels for workload role, environment, and tenant where applicable.
- Keep helm test pods observable enough to debug readiness and connectivity failures.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware charts.
- Run `helm lint`.
- Run `helm template` for dev and test and validate rendered output with kubeconform.
- Run `helm test` when the chart defines test hooks.

## Anti-Patterns

- Hiding provider-specific cloud resources inside Helm templates.
- Putting plaintext secrets in values files.
- Using one chart value to switch between unrelated workload roles.
- Letting dev and test share release names or namespaces.
