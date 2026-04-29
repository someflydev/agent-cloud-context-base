# EKS Base

Load this stack for AWS Kubernetes platforms on Amazon EKS. It owns the cluster boundary, node capacity model, AWS networking integrations, and accb Kubernetes validation gates.

## Cluster Surface

- Control plane: pin Kubernetes 1.30 or newer and record the patch version in IaC outputs.
- Node pools: start with managed node groups for system and application pools.
- Capacity: size dev with small burstable nodes and test with production-like instance families.
- Autoscaling: use cluster-autoscaler for managed node groups or Karpenter when consolidation and mixed capacity are required.
- Networking plugin: AWS VPC CNI with prefix delegation where pod density requires it.
- Ingress: AWS Load Balancer Controller with ALB Ingress for HTTP workloads.
- Load balancing: keep NLB explicit for non-HTTP protocols.
- Identity-to-pod: use IRSA through the cluster OIDC provider; consider EKS Pod Identity Agent where supported.
- Add-ons: pin CoreDNS, kube-proxy, VPC CNI, EBS CSI, and metrics-server versions.

## Workload Surface

- Compose this base with exactly one role pack per process class.
- APIs use `context/stacks/k8s-api-workload.md`.
- Queue consumers use `context/stacks/k8s-worker-workload.md`.
- One-off batch uses `context/stacks/k8s-job-workload.md`.
- Schedules use `context/stacks/k8s-cronjob-workload.md`.
- Reconcilers and controllers use `context/stacks/k8s-control-plane-workload.md`.
- Keep role-specific Kubernetes service accounts, probes, resources, and scaling rules.
- Use PodDisruptionBudget for workloads that must survive node replacement.
- Use topology spread constraints for highly available API and control-plane roles.

## Manifests / Charts

- Helm and Kustomize are both first-class in accb.
- Prefer Kustomize when overlays are simple and generated repos need plain YAML review.
- Prefer Helm when multiple roles share templated defaults or release packaging matters.
- Use `context/stacks/k8s-helm-conventions.md` for chart layout.
- Use `context/stacks/k8s-kustomize-conventions.md` for base and overlay layout.
- Keep dev and test namespaces, release names, image tags, and secret paths separate.
- Never share Kubernetes context names or kubeconfig assumptions between dev and test.

## Networking

- Declare VPC, subnet, route table, and security group ownership in IaC.
- Use private subnets for worker nodes unless a public-node exception is documented.
- Restrict API endpoint access to approved CIDRs or private connectivity when feasible.
- Use ALB security groups for ingress and least-privilege node security groups for pod egress.
- Add NetworkPolicy when the CNI or policy engine supports enforcement.
- For tenant-aware workloads, pair namespaces with ResourceQuota, LimitRange, and NetworkPolicy.

## Identity Binding

- Reference `context/stacks/identity-aws-iam.md` for IAM, IRSA, and pod identity guidance.
- Create one IAM role per workload role unless a manifest justifies sharing.
- Bind service accounts to IAM roles with explicit subject and namespace.
- Scope SQS, SNS, EventBridge, DynamoDB, S3, RDS, Secrets Manager, and KMS access by environment.
- Keep dev and test IAM roles, OIDC bindings, and resource ARNs disjoint.

## Secrets

- Use External Secrets Operator for Kubernetes Secret materialization.
- Reference `context/stacks/secrets-aws-secrets-manager.md` when PROMPT_12 adds the provider secret stack.
- Store secret source paths under environment-specific prefixes.
- Do not commit Kubernetes Secret manifests with plaintext data.
- Give each workload role only the secret reads it requires.

## Observability

- Reference `context/stacks/observability-otel-cloud.md` and `context/stacks/k8s-otel-collector.md`.
- Emit structured logs with cluster, namespace, workload role, pod, container, trace id, and tenant where applicable.
- Export traces, metrics, and logs to CloudWatch or the selected OpenTelemetry backend.
- Scrape Kubernetes and workload metrics needed for HPA, KEDA, rollout, and SLO checks.

## Validation Gates (cross-reference)

- `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, and `k8s-tenant-isolation-evident` when namespaces carry tenant boundaries.
- `eks-cluster-reachable` from `context/accb/profile-rules.json`.
- Prove rollback by changing an immutable image tag and reverting to a previous digest.

## Anti-Patterns

- Running all process classes in one Deployment.
- Sharing one IAM role across unrelated Kubernetes service accounts.
- Treating ALB reachability as readiness.
- Rebuilding images during test promotion instead of promoting immutable digests.
