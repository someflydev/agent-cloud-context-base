# K8s Stack Surface

PROMPT_11 added the Kubernetes stack surface for accb.

The cluster base files are:

- `context/stacks/eks-base.md`
- `context/stacks/gke-base.md`
- `context/stacks/aks-base.md`

The provider-agnostic role pack files are:

- `context/stacks/k8s-api-workload.md`
- `context/stacks/k8s-worker-workload.md`
- `context/stacks/k8s-job-workload.md`
- `context/stacks/k8s-cronjob-workload.md`
- `context/stacks/k8s-control-plane-workload.md`

The supporting Kubernetes convention files are:

- `context/stacks/k8s-helm-conventions.md`
- `context/stacks/k8s-kustomize-conventions.md`
- `context/stacks/k8s-otel-collector.md`
- `context/stacks/k8s-keda-autoscaling.md`

These 12 files establish the Kubernetes runtime tier surface through EKS, GKE, AKS, workload roles, manifest packaging, in-cluster telemetry, and KEDA autoscaling.

PROMPT_12 adds IaC and cross-cutting stacks, including provider secret store stacks referenced by these Kubernetes files.
