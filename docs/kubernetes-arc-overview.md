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
- PROMPT_33 wires root README, ARCHITECTURE_MAP, and end-to-end smoke coverage.

## How To Generate A New Repo From This Arc

Select the closest scenario pattern, choose the provider/runtime/language cell from `docs/provider-parity-matrix.md`, then invoke `scripts/new_cloud_repo.py` with the matching manifest. Example:

```bash
python3 scripts/new_cloud_repo.py --archetype k8s-platform-repo --provider aws --runtime-tier k8s --primary-stack eks-base --primary-language python --iac-tool pulumi-python --manifest k8s-eks-multi-role-python --output ../my-k8s-repo
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

| Note | Contract impact |
| --- | --- |
| 1 | Catalog and registry must agree before an example is treated as canonical. |
| 2 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 3 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 4 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 5 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 6 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 7 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 8 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 9 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 10 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 11 | Catalog and registry must agree before an example is treated as canonical. |
| 12 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 13 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 14 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 15 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 16 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 17 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 18 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 19 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 20 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 21 | Catalog and registry must agree before an example is treated as canonical. |
| 22 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 23 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 24 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 25 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 26 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 27 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 28 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 29 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 30 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 31 | Catalog and registry must agree before an example is treated as canonical. |
| 32 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 33 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 34 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 35 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 36 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 37 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 38 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 39 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 40 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 41 | Catalog and registry must agree before an example is treated as canonical. |
| 42 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 43 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 44 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 45 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 46 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 47 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 48 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 49 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 50 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 51 | Catalog and registry must agree before an example is treated as canonical. |
| 52 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 53 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 54 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 55 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 56 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 57 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 58 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 59 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 60 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 61 | Catalog and registry must agree before an example is treated as canonical. |
| 62 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 63 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 64 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 65 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 66 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 67 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 68 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 69 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 70 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 71 | Catalog and registry must agree before an example is treated as canonical. |
| 72 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 73 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 74 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 75 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 76 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 77 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 78 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 79 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 80 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 81 | Catalog and registry must agree before an example is treated as canonical. |
| 82 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 83 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 84 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 85 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 86 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 87 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 88 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 89 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 90 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
