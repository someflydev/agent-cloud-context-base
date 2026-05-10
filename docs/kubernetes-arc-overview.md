# Kubernetes Arc Overview

## Arc Goal

The Kubernetes arc demonstrates multi-role platform repositories across EKS, GKE, and AKS, including API, worker, job, and cronjob surfaces with Helm values, role separation, and provider-specific identity and storage anchors.

## Examples Authored

- aws x python: `canonical-eks/multi-role-platform`
- aws x go: `canonical-eks/multi-role-platform`
- gcp x python: `canonical-gke/multi-role-platform`
- gcp x go: `canonical-gke/multi-role-platform`
- azure x dotnet: `canonical-aks/multi-role-platform`
- azure x typescript: `canonical-aks/multi-role-platform`

## Doctrines Anchored

- `context/doctrine/k8s-workload-role-separation.md`
- `context/doctrine/k8s-multi-tenancy-and-namespacing.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/observability-cloud-native.md`
- `context/doctrine/testing-philosophy-cloud.md`

## Stacks Anchored

- `context/stacks/eks-base.md`
- `context/stacks/gke-base.md`
- `context/stacks/aks-base.md`
- `context/stacks/k8s-api-workload.md`
- `context/stacks/k8s-worker-workload.md`
- `context/stacks/k8s-job-workload.md`
- `context/stacks/k8s-cronjob-workload.md`
- `context/stacks/k8s-helm-conventions.md`
- `context/stacks/k8s-kustomize-conventions.md`

## Workflows Anchored

- `context/skills/k8s-workload-role-decomposition.md`

## Scenario Patterns Covered

| Scenario pattern | Canonical example families |
| --- | --- |
| `k8s.multi-role-platform` | `canonical-aks`, `canonical-eks`, `canonical-gke` |
| `k8s.stream-replay-platform` | `canonical-aks`, `canonical-eks`, `canonical-gke` |
| `k8s.rag-knowledge-mesh` | `canonical-aks`, `canonical-eks`, `canonical-gke` |
| `k8s.regulated-document-platform` | `canonical-aks`, `canonical-eks`, `canonical-gke` |
| `k8s.workflow-control-plane` | `canonical-aks`, `canonical-eks`, `canonical-gke` |
| `k8s.heterogeneous-compute-platform` | `canonical-aks`, `canonical-eks`, `canonical-gke` |

## Validation Gates

| Gate ID | Covering example |
| --- | --- |
| `kubernetes-gate-01` | smoke verify.sh: `canonical-eks/multi-role-platform/python` |
| `kubernetes-gate-02` | structured-log-shape: `canonical-eks/multi-role-platform/go` |
| `kubernetes-gate-03` | terraform dev/test isolation: `canonical-gke/multi-role-platform/python` |
| `kubernetes-gate-04` | pulumi stack isolation: `canonical-gke/multi-role-platform/go` |
| `kubernetes-gate-05` | replay fixtures: `canonical-aks/multi-role-platform/dotnet` |
| `kubernetes-gate-06` | lane-a local provider: `canonical-aks/multi-role-platform/typescript` |
| `kubernetes-gate-07` | lane-b ephemeral real cloud: `canonical-eks/multi-role-platform/python` |

## Lane Coverage

| Example | Lane A | Lane B | Lane C |
| --- | --- | --- | --- |
| `canonical-eks/multi-role-platform/python` | yes | yes | deferred |
| `canonical-eks/multi-role-platform/go` | yes | yes | deferred |
| `canonical-gke/multi-role-platform/python` | yes | yes | deferred |
| `canonical-gke/multi-role-platform/go` | yes | yes | deferred |
| `canonical-aks/multi-role-platform/dotnet` | yes | yes | deferred |
| `canonical-aks/multi-role-platform/typescript` | yes | yes | deferred |

## Verification Status

Authoritative tier metadata lives in `verification/example_registry.yaml`; this
table is a human summary.

| Example | Smoke | Local provider | Real cloud | Full |
| --- | --- | --- | --- | --- |
| `canonical-eks/multi-role-platform/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-eks/multi-role-platform/go` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gke/multi-role-platform/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gke/multi-role-platform/go` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aks/multi-role-platform/dotnet` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aks/multi-role-platform/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |

## Known Gaps + Follow-on Arcs

- Real-cloud Lane B remains operator-gated because it can create billable resources.
- Lane C full release gates are represented only where a canonical release gate exists.
- Deferred scenario patterns in `context/scenarios/scenario-profile-map.yaml` must be promoted by later example-authoring arcs.
- Provider local bundles are harness contracts here; derived repos own provider-specific fixture depth.

## How To Generate A New Repo From This Arc

Select the closest scenario pattern, choose the provider/runtime/language cell from `docs/provider-parity-matrix.md`, then invoke `scripts/new_cloud_repo.py` with the matching manifest. Example:

```bash
python3 scripts/new_cloud_repo.py --archetype k8s-platform-repo --provider aws --runtime-tier k8s --primary-stack eks-base --primary-language python --iac-tool pulumi-python --manifest k8s-eks-multi-role-python --target-dir ../my-k8s-repo
```

## Registry Detail

| Family | Provider | Runtime | Language | Terraform | Pulumi | Dev/test disjoint |
| --- | --- | --- | --- | --- | --- | --- |
| `canonical-eks` | aws | k8s | python | True | pulumi-python | True |
| `canonical-eks` | aws | k8s | go | True | pulumi-go | True |
| `canonical-gke` | gcp | k8s | python | True | pulumi-python | True |
| `canonical-gke` | gcp | k8s | go | True | pulumi-go | True |
| `canonical-aks` | azure | k8s | dotnet | True | pulumi-dotnet | True |
| `canonical-aks` | azure | k8s | typescript | True | pulumi-typescript | True |

## Arc Operating Notes

- Catalog and registry must agree before an example is treated as canonical.
- IaC isolation is validated through the shared script, not per-family bespoke logic.
- Lane A local-provider checks remain explicitly gated by environment variables.
- Lane B real-cloud checks remain explicitly gated because they can create billable resources.
- Structured logs are part of the runtime contract for examples with executable workloads.
- Scenario patterns may point at deferred examples only when the map declares the deferral.
- Generated repos should load manifests first and broaden context only when routing requires it.
- Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other.
- Provider-specific runtime behavior is allowed when the example README owns the reason.
