# agent-cloud-context-base (accb)

`agent-cloud-context-base` (`accb`) is a context-first foundation for generating and running assistant-friendly cloud-native backend repositories across serverless functions, managed containers, Kubernetes platforms, and explicit Infrastructure as Code surfaces.

## Start Here By Goal

| Goal | Read first | Doc of the day | CLI command |
| --- | --- | --- | --- |
| Understand the base | [`AGENT.md`](AGENT.md) | [`docs/context-boot-sequence.md`](docs/context-boot-sequence.md) | `python3 scripts/work.py resume` |
| Generate a new repo | [`AGENT.md`](AGENT.md) | [`docs/usage/STARTING_NEW_PROJECTS.md`](docs/usage/STARTING_NEW_PROJECTS.md) | `python3 scripts/new_cloud_repo.py --help` |
| Turn a workload scenario into a profile | [`context/router/scenario-router.md`](context/router/scenario-router.md) | [`context/workflows/plan-scenario-derived-repo.md`](context/workflows/plan-scenario-derived-repo.md) | `python3 scripts/accb_payload.py --help` |
| Work inside a generated repo | `.accb/SESSION_BOOT.md` in the derived repo | [`docs/usage/ASSISTANT_BEHAVIOR_SPEC.md`](docs/usage/ASSISTANT_BEHAVIOR_SPEC.md) | `python3 .accb/scripts/accb_verify.py` |
| Browse canonical examples | [`examples/README.md`](examples/README.md) | [`examples/catalog.json`](examples/catalog.json) | `python3 scripts/verify_examples.py --family canonical-aws-lambda` |
| Verify the repo | [`verification/README.md`](verification/README.md) | [`docs/ARCHITECTURE_MAP.md`](docs/ARCHITECTURE_MAP.md) | `python3 scripts/run_verification.py --tier fast` |

## What Problem It Solves

- Assistant drift: `context/accb/profile-rules.json`, routers, and manifest bundles keep sessions tied to a declared provider, runtime tier, language, and IaC tool.
- Repo intent rediscovery: `scripts/work.py resume`, checkpoints, and memory artifacts make session state explicit instead of forcing each assistant to infer the repo from scratch.
- Pattern improvisation: canonical examples, scenario patterns, stack packs, and workflows point assistants at proven cloud patterns before they invent a new one.
- Opaque generation: generated repos receive a `.accb/` payload with profile selection, validation gates, specs, and a boot document that explains what was composed and why.

## Canonical Examples

| Family | What it shows | Providers | Languages | IaC tools | Catalog entry |
| --- | --- | --- | --- | --- | --- |
| `canonical-aws-lambda` | AWS Lambda event and HTTP handlers with replay, secrets, and dev/test isolation | aws | go, python, typescript | Pulumi Go/Python/TypeScript, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-gcp-functions` | GCP Cloud Functions for storage, HTTP, Pub/Sub, Eventarc, and Firebase triggers | gcp | go, python, typescript | Pulumi Go/Python/TypeScript, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-azure-functions` | Azure Functions with Blob, Service Bus, Cosmos change feed, and Event Grid triggers | azure | dotnet-isolated, python, typescript | Pulumi .NET/Python/TypeScript, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-cloud-run` | Cloud Run APIs, workers, jobs, and sidecars | gcp | go, python, typescript | Pulumi Go/Python/TypeScript, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-app-runner` | App Runner services with VPC connector and onboarding flows | aws | go, python | Pulumi Go/Python, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-container-apps` | Azure Container Apps APIs, workers, jobs, and Dapr binding patterns | azure | dotnet-aspnet, python, typescript-hono | Pulumi .NET/Python/TypeScript, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-eks`, `canonical-gke`, `canonical-aks` | Multi-role Kubernetes platforms with API, worker, job, cron, Helm, Kustomize, and IaC | aws, gcp, azure | dotnet, go, python, typescript | Pulumi .NET/Go/Python/TypeScript, Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-iac-terraform` | Provider-specific Terraform module starters with disjoint dev/test state | aws, azure, gcp | terraform | Terraform | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-iac-pulumi` | Pulumi starters across providers and languages | aws, azure, gcp | dotnet, go, python, typescript | Pulumi .NET/Go/Python/TypeScript | [`examples/catalog.json`](examples/catalog.json) |
| `canonical-eventing`, `canonical-observability`, `canonical-secrets`, `canonical-prompts` | Cross-cutting reference packs for eventing, telemetry, secrets, and prompt-first delivery | multi | multi, text | reference | [`examples/catalog.json`](examples/catalog.json) |

Detailed tier status lives in [`verification/example_registry.yaml`](verification/example_registry.yaml).

## Scenario Catalog

`context/scenarios/` distills the excellent-cloud prompt catalogs into workload patterns. Start with [`context/scenarios/scenario-profile-map.yaml`](context/scenarios/scenario-profile-map.yaml), route natural-language prompts through [`context/router/scenario-router.md`](context/router/scenario-router.md), then execute [`context/workflows/plan-scenario-derived-repo.md`](context/workflows/plan-scenario-derived-repo.md) to turn a scenario into a concrete profile.

## First-Class Coverage

| Provider | Function | Managed container | Kubernetes | IaC |
| --- | --- | --- | --- | --- |
| AWS | Lambda: Python, TypeScript, Go | App Runner: Python FastAPI, Go Echo | EKS: Python, Go | Terraform, Pulumi TypeScript/Python/Go |
| GCP | Cloud Functions: Python, TypeScript, Go | Cloud Run: Python FastAPI, Go Echo, TypeScript Hono, jobs, sidecars | GKE: Python, Go | Terraform, Pulumi TypeScript/Python/Go |
| Azure | Azure Functions: Python, TypeScript, .NET isolated | Container Apps: Python FastAPI, .NET ASP.NET, TypeScript Hono, Dapr, jobs | AKS: .NET, TypeScript | Terraform, Pulumi TypeScript/Python/.NET |

See [`docs/provider-parity-matrix.md`](docs/provider-parity-matrix.md) for the full support matrix and deferred cells.

## Docs Index

| Area | Docs |
| --- | --- |
| Architecture and design | [`docs/ARCHITECTURE_MAP.md`](docs/ARCHITECTURE_MAP.md), [`docs/architecture/ASSISTANT_RUNTIME_MODEL.md`](docs/architecture/ASSISTANT_RUNTIME_MODEL.md), [`docs/architecture/CONTEXT_ENGINEERING_GUIDE.md`](docs/architecture/CONTEXT_ENGINEERING_GUIDE.md) |
| Operator usage | [`docs/usage/STARTING_NEW_PROJECTS.md`](docs/usage/STARTING_NEW_PROJECTS.md), [`docs/usage/SPEC_DRIVEN_ACCB_PAYLOADS.md`](docs/usage/SPEC_DRIVEN_ACCB_PAYLOADS.md), [`docs/usage/ADVANCED_ASSISTANT_OPERATIONS.md`](docs/usage/ADVANCED_ASSISTANT_OPERATIONS.md), [`docs/usage/ASSISTANT_BEHAVIOR_SPEC.md`](docs/usage/ASSISTANT_BEHAVIOR_SPEC.md) |
| Session startup and continuity | [`docs/session-start.md`](docs/session-start.md), [`docs/context-boot-sequence.md`](docs/context-boot-sequence.md), [`docs/runtime-state-workflow.md`](docs/runtime-state-workflow.md), [`docs/memory-layer-overview.md`](docs/memory-layer-overview.md) |
| Arc overviews | [`docs/functions-arc-overview.md`](docs/functions-arc-overview.md), [`docs/containers-arc-overview.md`](docs/containers-arc-overview.md), [`docs/kubernetes-arc-overview.md`](docs/kubernetes-arc-overview.md) |
| Reference | [`docs/repo-purpose.md`](docs/repo-purpose.md), [`docs/repo-layout.md`](docs/repo-layout.md), [`scripts/README.md`](scripts/README.md), [`manifests/README.md`](manifests/README.md), [`verification/README.md`](verification/README.md) |
| Isolation and parity | [`docs/iac-isolation-contract.md`](docs/iac-isolation-contract.md), [`docs/provider-parity-matrix.md`](docs/provider-parity-matrix.md) |

## Verification Commands

```bash
python3 scripts/validate_context.py
python3 scripts/validate_manifests.py
python3 scripts/validate_iac_isolation.py <iac-dir>
python3 scripts/run_verification.py --tier fast
python3 scripts/run_verification.py --tier medium --update-registry
python3 scripts/accb_payload.py --archetype cloud-function-repo \
  --primary-stack aws-lambda-python --primary-language python \
  --provider aws --runtime-tier function --iac-tool pulumi-python \
  --manifest func-aws-lambda-python --output-dir /tmp/accb-smoke
```
