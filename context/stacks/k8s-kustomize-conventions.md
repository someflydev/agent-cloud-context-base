# K8s Kustomize Conventions

Load this stack when a generated Kubernetes repo uses Kustomize as the first-class manifest overlay system. It defines base resources, environment overlays, generators, secret policy, and validation expectations.

## Cluster Surface

- Compose Kustomize overlays with exactly one cluster base: `eks-base.md`, `gke-base.md`, or `aks-base.md`.
- Keep `base/` provider-neutral unless a selected cluster base requires provider-specific resources.
- Use `overlays/dev/` and `overlays/test/` for environment differences.
- Keep namespaces, name prefixes, labels, image digests, and secret source refs separate for dev and test.
- Use Kustomize only for rendered Kubernetes objects; cloud resources stay in Terraform or Pulumi.

## Workload Surface

- Each role base declares its Kubernetes kind explicitly.
- API bases include Deployment, Service, optional HPA, optional PDB, and ServiceAccount.
- Worker bases include Deployment, KEDA ScaledObject, ServiceAccount, and optional PDB.
- Job bases include Job with parallelism, completions, deadline, backoff, and TTL.
- CronJob bases include schedule, concurrencyPolicy, deadlines, and history limits.
- Control-plane bases include Deployment, leader election settings, RBAC, and optional webhook Service.
- All bases set probes, resources, labels, and securityContext by default.

## Manifests / Charts

- Required layout: `base/kustomization.yaml`, role manifests under `base/`, `overlays/dev/kustomization.yaml`, and `overlays/test/kustomization.yaml`.
- Use `namePrefix` or explicit names to make environment ownership obvious.
- Use `commonLabels` for `app.kubernetes.io/part-of`, role component, environment, and tenant where applicable.
- Use `images` to pin repository and digest in overlays.
- Use patches for resources, scaling, schedules, and ingress differences.
- Keep generated output reviewable with `kustomize build`.
- Do not duplicate full base manifests in overlays.

## Networking

- Keep Services as ClusterIP unless a role pack and cluster base say otherwise.
- Place Ingress, HTTPRoute, or provider-specific annotations in overlays.
- Put TLS hostnames and certificate references in environment overlays.
- Include NetworkPolicy in base when the workload should always be private.
- Use overlays for tenant-aware namespace policy and provider-specific ingress classes.

## Identity Binding

- Define ServiceAccounts in base per role.
- Patch provider identity annotations in dev and test overlays.
- Reference `identity-aws-iam.md`, `identity-gcp-iam-sa.md`, or `identity-azure-entra-mi.md` through the cluster base.
- Keep Role, ClusterRole, and binding manifests scoped to the role pack contract.
- Do not use cluster-wide RBAC unless the role pack requires it.

## Secrets

- Use External Secrets Operator for secret injection.
- Reference `context/stacks/secrets-aws-secrets-manager.md`, `context/stacks/secrets-gcp-secret-manager.md`, or `context/stacks/secrets-azure-key-vault.md` for the selected provider.
- Use ExternalSecret manifests or patches with environment-specific remote refs.
- Use `configMapGenerator` for non-secret config only.
- Avoid `secretGenerator` for real secrets; it is acceptable only for local non-sensitive fixtures.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Add annotations, env, ports, and ServiceMonitor or PodMonitor resources only when the selected observability path supports them.
- Keep telemetry labels consistent across base and overlays.
- Make rendered manifests carry environment and tenant labels for log and metric joins.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` for tenant-aware overlays.
- Run `kustomize build overlays/dev` and `kustomize build overlays/test`.
- Pipe rendered output to kubeconform.
- Review rendered output for plaintext secret values.

## Anti-Patterns

- Copying whole bases into overlays.
- Using generators for production secret values.
- Letting dev and test share names, namespaces, or image tags.
- Hiding provider-specific behavior in unexplained patches.
