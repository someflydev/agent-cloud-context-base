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
| `containers-gate-01` | smoke verify.sh: `canonical-cloud-run/public-api-private-worker-job/python-fastapi` |
| `containers-gate-02` | structured-log-shape: `canonical-cloud-run/multi-container-sidecar/python-fastapi` |
| `containers-gate-03` | terraform dev/test isolation: `canonical-cloud-run/public-api-private-worker-job/go-echo` |
| `containers-gate-04` | pulumi stack isolation: `canonical-cloud-run/public-api-private-worker-job/typescript-hono` |
| `containers-gate-05` | replay fixtures: `canonical-cloud-run/cloudrun-job-nightly-report/python-fastapi` |
| `containers-gate-06` | lane-a local provider: `canonical-app-runner/public-api-with-vpc-connector/python-fastapi` |
| `containers-gate-07` | lane-b ephemeral real cloud: `canonical-app-runner/public-api-with-vpc-connector/go-echo` |

## Lane Coverage

| Example | Lane A | Lane B | Lane C |
| --- | --- | --- | --- |
| `canonical-cloud-run/public-api-private-worker-job/python-fastapi` | yes | yes | deferred |
| `canonical-cloud-run/multi-container-sidecar/python-fastapi` | yes | yes | deferred |
| `canonical-cloud-run/public-api-private-worker-job/go-echo` | yes | yes | deferred |
| `canonical-cloud-run/public-api-private-worker-job/typescript-hono` | yes | yes | deferred |
| `canonical-cloud-run/cloudrun-job-nightly-report/python-fastapi` | yes | yes | deferred |
| `canonical-app-runner/public-api-with-vpc-connector/python-fastapi` | yes | yes | deferred |
| `canonical-app-runner/public-api-with-vpc-connector/go-echo` | yes | yes | deferred |
| `canonical-app-runner/supplier-onboarding/python-fastapi` | yes | yes | deferred |
| `canonical-container-apps/public-api-private-worker-jobs/python-fastapi` | yes | yes | deferred |
| `canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet` | yes | yes | deferred |
| `canonical-container-apps/public-api-private-worker-jobs/dotnet-aspnet` | yes | yes | deferred |
| `canonical-container-apps/public-api-private-worker-jobs/typescript-hono` | yes | yes | deferred |

## Verification Status

Authoritative tier metadata lives in `verification/example_registry.yaml`; this
table is a human summary.

| Example | Smoke | Local provider | Real cloud | Full |
| --- | --- | --- | --- | --- |
| `canonical-cloud-run/public-api-private-worker-job/python-fastapi` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/multi-container-sidecar/python-fastapi` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/public-api-private-worker-job/go-echo` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/public-api-private-worker-job/typescript-hono` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-cloud-run/cloudrun-job-nightly-report/python-fastapi` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-app-runner/public-api-with-vpc-connector/python-fastapi` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-app-runner/public-api-with-vpc-connector/go-echo` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-app-runner/supplier-onboarding/python-fastapi` | skipped<br>docker daemon unavailable in current environment | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/public-api-private-worker-jobs/python-fastapi` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/public-api-private-worker-jobs/dotnet-aspnet` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-container-apps/public-api-private-worker-jobs/typescript-hono` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |

## Known Gaps + Follow-on Arcs

- Real-cloud Lane B remains operator-gated because it can create billable resources.
- Lane C full release gates are represented only where a canonical release gate exists.
- Deferred scenario patterns in `context/scenarios/scenario-profile-map.yaml` must be promoted by later example-authoring arcs.
- Provider local bundles are harness contracts here; derived repos own provider-specific fixture depth.

## How To Generate A New Repo From This Arc

Select the closest scenario pattern, choose the provider/runtime/language cell from `docs/provider-parity-matrix.md`, then invoke `scripts/new_cloud_repo.py` with the matching manifest. Example:

```bash
python3 scripts/new_cloud_repo.py --archetype managed-container-multi-service --provider gcp --runtime-tier managed_container --primary-stack cloudrun-python-fastapi --primary-language python --iac-tool terraform --manifest container-cloudrun-fastapi --target-dir ../my-container-repo
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

- Catalog and registry must agree before an example is treated as canonical.
- IaC isolation is validated through the shared script, not per-family bespoke logic.
- Lane A local-provider checks remain explicitly gated by environment variables.
- Lane B real-cloud checks remain explicitly gated because they can create billable resources.
- Structured logs are part of the runtime contract for examples with executable workloads.
- Scenario patterns may point at deferred examples only when the map declares the deferral.
- Generated repos should load manifests first and broaden context only when routing requires it.
- Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other.
- Provider-specific runtime behavior is allowed when the example README owns the reason.
