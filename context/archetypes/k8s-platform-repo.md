# K8s Platform Repo

Use this archetype for an EKS, GKE, or AKS repository where API, worker, job, cron, and optional control-plane roles are structural. Kubernetes is warranted when independent scaling, recovery, rollout behavior, workload identity, and platform topology are first-class requirements rather than future possibilities.

## Common Goals

- Model each workload role as a distinct Kubernetes controller.
- Use Helm or Kustomize overlays for dev and test differences.
- Declare cluster and workload-identity isolation explicitly.
- Keep queue, storage, secret, and observability seams provider-native.
- Prove rollout, rollback, job completion, cron behavior, and worker recovery.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/k8s-workload-role-separation.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+k8s+language stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-eks/`, `examples/canonical-gke/`, or `examples/canonical-aks/`

## Common Workflows

- `context/workflows/add-k8s-workload-role.md`
- `context/workflows/add-helm-or-kustomize-overlay.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-replay-and-dlq-handling.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/k8s-eks-multi-role-python.yaml`
- `manifests/k8s-eks-multi-role-go.yaml`
- `manifests/k8s-gke-multi-role-python.yaml`
- `manifests/k8s-aks-multi-role-dotnet.yaml`

## Likely Examples

- `examples/canonical-eks/multi-role-platform/`
- `examples/canonical-gke/stream-replay-platform/`
- `examples/canonical-aks/workflow-control-plane/`

## Typical Anti-Patterns

- Collapsing API, worker, job, and cron roles into one Deployment.
- Granting cluster-wide RBAC to tenant or application code.
- Using one service account for every workload role.
- Treating overlays as copy-pasted manifests with drift.
- Skipping rollback validation because rollout succeeded once.

## Validation Gates (summary)

- k8s-role-separation-evident: API, worker, job, and cron live in distinct workloads.
- k8s-rolling-rollout-and-rollback-paths: Rolling update and rollback both succeed in test.
- eventing-dlq-path: Worker DLQ path is exercised.
- iac-dev-test-disjoint: Cluster, namespace, state, and identity names are disjoint.
