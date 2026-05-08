# Containers Arc Overview

## Arc Goal

The managed-container arc captures long-running service, private worker, sidecar, job, Dapr, and VPC connector patterns across Cloud Run, App Runner, and Azure Container Apps while preserving accb deployment, observability, and dev/test isolation requirements.

## Examples Authored

- gcp x python: `canonical-cloud-run/public-api-private-worker-job`
- gcp x python: `canonical-cloud-run/multi-container-sidecar`
- gcp x go: `canonical-cloud-run/public-api-private-worker-job`
- gcp x typescript: `canonical-cloud-run/public-api-private-worker-job`
- gcp x python: `canonical-cloud-run/cloudrun-job-nightly-report`
- aws x python: `canonical-app-runner/public-api-with-vpc-connector`
- aws x go: `canonical-app-runner/public-api-with-vpc-connector`
- aws x python: `canonical-app-runner/supplier-onboarding`
- azure x python: `canonical-container-apps/public-api-private-worker-jobs`
- azure x dotnet-aspnet: `canonical-container-apps/dapr-pubsub-binding`
- azure x dotnet-aspnet: `canonical-container-apps/public-api-private-worker-jobs`
- azure x typescript-hono: `canonical-container-apps/public-api-private-worker-jobs`

## Doctrines Anchored

- `context/doctrine/container-image-discipline.md`
- `context/doctrine/managed-service-selection.md`
- `context/doctrine/vpc-and-private-networking.md`
- `context/doctrine/observability-cloud-native.md`
- `context/doctrine/testing-philosophy-cloud.md`

## Stacks Anchored

- `context/stacks/cloudrun-python-fastapi.md`
- `context/stacks/cloudrun-go-echo.md`
- `context/stacks/cloudrun-typescript-hono.md`
- `context/stacks/cloudrun-job.md`
- `context/stacks/apprunner-python-fastapi.md`
- `context/stacks/apprunner-go-echo.md`
- `context/stacks/apprunner-vpc-connector.md`
- `context/stacks/aca-python-fastapi.md`
- `context/stacks/aca-dotnet-aspnet.md`
- `context/stacks/aca-dapr.md`
- `context/stacks/aca-jobs.md`

## Workflows Anchored

- `context/workflows/add-cloud-database-integration.md`

## Scenario Patterns Covered

| Scenario pattern | Canonical example families |
| --- | --- |
| `container.public-api-private-worker-job` | `canonical-app-runner`, `canonical-cloud-run`, `canonical-container-apps` |
| `container.heavy-runtime-service` | `canonical-app-runner`, `canonical-cloud-run`, `canonical-container-apps` |
| `container.partner-adapter-gateway` | `canonical-app-runner`, `canonical-cloud-run`, `canonical-container-apps` |
| `container.multi-container-sidecar` | `canonical-cloud-run`, `canonical-container-apps` |
| `container.job-first-container` | `canonical-cloud-run`, `canonical-container-apps` |

## Validation Gates

| Gate ID | Covering example |
| --- | --- |
| `containers-gate-01` | smoke verify.sh: `canonical-cloud-run/public-api-private-worker-job/python` |
| `containers-gate-02` | structured-log-shape: `canonical-cloud-run/multi-container-sidecar/python` |
| `containers-gate-03` | terraform dev/test isolation: `canonical-cloud-run/public-api-private-worker-job/go` |
| `containers-gate-04` | pulumi stack isolation: `canonical-cloud-run/public-api-private-worker-job/typescript` |
| `containers-gate-05` | replay fixtures: `canonical-cloud-run/cloudrun-job-nightly-report/python` |
| `containers-gate-06` | lane-a local provider: `canonical-app-runner/public-api-with-vpc-connector/python` |
| `containers-gate-07` | lane-b ephemeral real cloud: `canonical-app-runner/public-api-with-vpc-connector/go` |

## Lane Coverage

| Example | Lane A | Lane B | Lane C |
| --- | --- | --- | --- |
| `canonical-cloud-run/public-api-private-worker-job/python` | yes | yes | deferred |
| `canonical-cloud-run/multi-container-sidecar/python` | yes | yes | deferred |
| `canonical-cloud-run/public-api-private-worker-job/go` | yes | yes | deferred |
| `canonical-cloud-run/public-api-private-worker-job/typescript` | yes | yes | deferred |
| `canonical-cloud-run/cloudrun-job-nightly-report/python` | yes | yes | deferred |
| `canonical-app-runner/public-api-with-vpc-connector/python` | yes | yes | deferred |
| `canonical-app-runner/public-api-with-vpc-connector/go` | yes | yes | deferred |
| `canonical-app-runner/supplier-onboarding/python` | yes | yes | deferred |
| `canonical-container-apps/public-api-private-worker-jobs/python` | yes | yes | deferred |
| `canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet` | yes | yes | deferred |
| `canonical-container-apps/public-api-private-worker-jobs/dotnet-aspnet` | yes | yes | deferred |
| `canonical-container-apps/public-api-private-worker-jobs/typescript-hono` | yes | yes | deferred |

## Verification Status

| Example | Smoke | Local provider | Real cloud | Full |
| --- | --- | --- | --- | --- |
| `canonical-cloud-run/public-api-private-worker-job/python` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/multi-container-sidecar/python` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/public-api-private-worker-job/go` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/public-api-private-worker-job/typescript` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/cloudrun-job-nightly-report/python` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-app-runner/public-api-with-vpc-connector/python` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-app-runner/public-api-with-vpc-connector/go` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-app-runner/supplier-onboarding/python` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/public-api-private-worker-jobs/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/public-api-private-worker-jobs/dotnet-aspnet` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/public-api-private-worker-jobs/typescript-hono` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |

## Known Gaps + Follow-on Arcs

- Real-cloud Lane B remains operator-gated because it can create billable resources.
- Lane C full release gates are represented only where a canonical release gate exists.
- Deferred scenario patterns in `context/scenarios/scenario-profile-map.yaml` must be promoted by later example-authoring arcs.
- Provider local bundles are harness contracts here; derived repos own provider-specific fixture depth.
- PROMPT_33 wires root README, ARCHITECTURE_MAP, and end-to-end smoke coverage.

## How To Generate A New Repo From This Arc

Select the closest scenario pattern, choose the provider/runtime/language cell from `docs/provider-parity-matrix.md`, then invoke `scripts/new_cloud_repo.py` with the matching manifest. Example:

```bash
python3 scripts/new_cloud_repo.py --archetype managed-container-multi-service --provider gcp --runtime-tier managed_container --primary-stack cloudrun-python-fastapi --primary-language python --iac-tool terraform --manifest container-cloudrun-fastapi --output ../my-container-repo
```

## Registry Detail

| Family | Provider | Runtime | Language | Terraform | Pulumi | Dev/test disjoint |
| --- | --- | --- | --- | --- | --- | --- |
| `canonical-cloud-run` | gcp | managed_container | python | True | pulumi-python | True |
| `canonical-cloud-run` | gcp | managed_container | python | True | pulumi-python | True |
| `canonical-cloud-run` | gcp | managed_container | go | True | pulumi-go | True |
| `canonical-cloud-run` | gcp | managed_container | typescript | True | pulumi-typescript | True |
| `canonical-cloud-run` | gcp | managed_container | python | True | pulumi-python | True |
| `canonical-app-runner` | aws | managed_container | python | True | pulumi-python | True |
| `canonical-app-runner` | aws | managed_container | go | True | pulumi-go | True |
| `canonical-app-runner` | aws | managed_container | python | True | pulumi-python | True |
| `canonical-container-apps` | azure | managed_container | python | True | pulumi-python | True |
| `canonical-container-apps` | azure | managed_container | dotnet-aspnet | True | pulumi-dotnet | True |
| `canonical-container-apps` | azure | managed_container | dotnet-aspnet | True | pulumi-dotnet | True |
| `canonical-container-apps` | azure | managed_container | typescript-hono | True | pulumi-typescript | True |

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
