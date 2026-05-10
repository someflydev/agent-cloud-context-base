# Docs

Use this directory when you need the current operating model for `accb`, not
the full context corpus.

## Fast Path

1. Start with [`../README.md`](../README.md) for goals, supported surfaces, and
   common commands.
2. Read [`ARCHITECTURE_MAP.md`](ARCHITECTURE_MAP.md) for the system diagrams.
3. Read [`repo-layout.md`](repo-layout.md) when you need to know which
   directory owns a concept.
4. Read [`usage/STARTING_NEW_PROJECTS.md`](usage/STARTING_NEW_PROJECTS.md) when
   generating a derived cloud repo.

## Architecture

- [`ARCHITECTURE_MAP.md`](ARCHITECTURE_MAP.md) - shortest accurate map of the
  generation, payload, session, scenario, and future-expansion flows.
- [`architecture/ASSISTANT_RUNTIME_MODEL.md`](architecture/ASSISTANT_RUNTIME_MODEL.md)
  - runtime subsystems, proof points, and failure modes.
- [`architecture/CONTEXT_ENGINEERING_GUIDE.md`](architecture/CONTEXT_ENGINEERING_GUIDE.md)
  - practical routing, bundle, verification, and drift-control guidance.

## Operator Usage

- [`usage/STARTING_NEW_PROJECTS.md`](usage/STARTING_NEW_PROJECTS.md) - concrete
  `new_cloud_repo.py` examples for function, managed-container, and Kubernetes
  repos.
- [`usage/SPEC_DRIVEN_ACCB_PAYLOADS.md`](usage/SPEC_DRIVEN_ACCB_PAYLOADS.md) -
  how `.accb/` payloads are composed and verified.
- [`usage/ASSISTANT_BEHAVIOR_SPEC.md`](usage/ASSISTANT_BEHAVIOR_SPEC.md) -
  expected assistant behavior inside generated repos.
- [`usage/ADVANCED_ASSISTANT_OPERATIONS.md`](usage/ADVANCED_ASSISTANT_OPERATIONS.md)
  - less common inspection, routing, and continuity operations.

## Session And Continuity

- [`session-start.md`](session-start.md) - base-repo and generated-repo startup
  steps.
- [`context-boot-sequence.md`](context-boot-sequence.md) - diagrammed boot
  contract for narrow context loading.
- [`runtime-state-workflow.md`](runtime-state-workflow.md) - local task,
  session, memory, and checkpoint surfaces.
- [`memory-layer-overview.md`](memory-layer-overview.md) - durable concept
  artifacts versus gitignored runtime state.

## Cloud Arcs

- [`functions-arc-overview.md`](functions-arc-overview.md) - AWS Lambda, GCP
  Cloud Functions, and Azure Functions coverage.
- [`containers-arc-overview.md`](containers-arc-overview.md) - Cloud Run, App
  Runner, and Azure Container Apps coverage.
- [`kubernetes-arc-overview.md`](kubernetes-arc-overview.md) - EKS, GKE, and
  AKS multi-role platform coverage.

## Reference

- [`repo-purpose.md`](repo-purpose.md) - what the repo optimizes for and what it
  intentionally does not solve.
- [`repo-layout.md`](repo-layout.md) - directory ownership map.
- [`provider-parity-matrix.md`](provider-parity-matrix.md) - generated provider,
  runtime, language, and canonical-example support matrix.
- [`iac-isolation-contract.md`](iac-isolation-contract.md) - dev/test isolation
  rules for Terraform and Pulumi.
