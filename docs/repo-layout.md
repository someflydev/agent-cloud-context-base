# Repo Layout

The repository is organized so assistants can route a cloud workload, compose a narrow context bundle, generate a `.accb/` payload, and verify the resulting repo without rediscovering the system shape.

| Path | Role | Owning prompt | Deeper doc |
| --- | --- | --- | --- |
| [`README.md`](../README.md) | Human and assistant front door | PROMPT_33 | [`docs/ARCHITECTURE_MAP.md`](ARCHITECTURE_MAP.md) |
| [`AGENT.md`](../AGENT.md), [`CLAUDE.md`](../CLAUDE.md) | Minimal startup instructions | PROMPT_01/PROMPT_05 | [`docs/context-boot-sequence.md`](context-boot-sequence.md) |
| [`.prompts/`](../.prompts) | Prompt-first build arc | PROMPT_01-33 | [`docs/session-start.md`](session-start.md) |
| [`context/doctrine/`](../context/doctrine) | Durable cloud operating rules | PROMPT_02-03 | [`docs/architecture/CONTEXT_ENGINEERING_GUIDE.md`](architecture/CONTEXT_ENGINEERING_GUIDE.md) |
| [`context/anchors/`](../context/anchors) | Startup anchors for identity, isolation, loading, and integrity | PROMPT_03 | [`docs/context-boot-sequence.md`](context-boot-sequence.md) |
| [`context/specs/`](../context/specs/README.md) | Product, architecture, agent, and evolution specs | PROMPT_04 | [`docs/usage/SPEC_DRIVEN_ACCB_PAYLOADS.md`](usage/SPEC_DRIVEN_ACCB_PAYLOADS.md) |
| [`context/validation/`](../context/validation/README.md) | Validation narratives and gate source material | PROMPT_04 | [`docs/architecture/ASSISTANT_RUNTIME_MODEL.md`](architecture/ASSISTANT_RUNTIME_MODEL.md) |
| [`context/accb/`](../context/accb/README.md) | Machine-readable profile rules | PROMPT_04 | [`docs/usage/SPEC_DRIVEN_ACCB_PAYLOADS.md`](usage/SPEC_DRIVEN_ACCB_PAYLOADS.md) |
| [`context/router/`](../context/router) | Task, provider, runtime, stack, archetype, IaC, and scenario routing | PROMPT_06 | [`docs/context-boot-sequence.md`](context-boot-sequence.md) |
| [`context/archetypes/`](../context/archetypes) | Repo-shape guidance | PROMPT_07 | [`context/router/archetype-router.md`](../context/router/archetype-router.md) |
| [`context/scenarios/`](../context/scenarios) | Workload-pattern layer between archetypes/manifests and user-facing scenario prompts | PROMPT_07 | [`context/scenarios/README.md`](../context/scenarios/README.md) |
| [`context/skills/`](../context/skills) | Focused decision guides for provider, runtime, IaC, secrets, scenarios, and validation | PROMPT_08 | [`docs/architecture/CONTEXT_ENGINEERING_GUIDE.md`](architecture/CONTEXT_ENGINEERING_GUIDE.md) |
| [`context/stacks/`](../context/stacks) | Runtime, provider, IaC, identity, secrets, storage, eventing, observability, and Kubernetes stack packs | PROMPT_09-12 | [`docs/provider-parity-matrix.md`](provider-parity-matrix.md) |
| [`context/workflows/`](../context/workflows) | Task playbooks for generation, feature addition, integration tests, promotion, and refinement | PROMPT_13 | [`context/workflows/bootstrap-cloud-repo.md`](../context/workflows/bootstrap-cloud-repo.md) |
| [`manifests/`](../manifests) | Machine-readable profile bundles and generation defaults | PROMPT_14 | [`manifests/README.md`](../manifests/README.md) |
| [`templates/`](../templates) | Starter scaffolds copied or referenced by generation | PROMPT_15 | [`templates/README.md`](../templates/README.md) |
| [`scripts/`](../scripts) | Runtime continuity, generation, payload composition, inspection, and validation commands | PROMPT_05/PROMPT_16-17 | [`scripts/README.md`](../scripts/README.md) |
| [`examples/`](../examples/README.md) | Canonical examples across runtime tiers and cross-cutting concerns | PROMPT_18-31 | [`examples/catalog.json`](../examples/catalog.json) |
| [`verification/`](../verification/README.md) | Registry, parity runners, policy fixtures, and script tests | PROMPT_17/PROMPT_32 | [`verification/example_registry.yaml`](../verification/example_registry.yaml) |
| [`docs/`](../docs) | Operator docs, architecture maps, parity docs, and arc overviews | PROMPT_32-33 | [`docs/ARCHITECTURE_MAP.md`](ARCHITECTURE_MAP.md) |
| [`memory/`](../memory) | Durable concept artifacts plus gitignored sessions and summaries | PROMPT_05/PROMPT_33 | [`docs/memory-layer-overview.md`](memory-layer-overview.md) |
| [`context/TASK.example.md`](../context/TASK.example.md), [`context/SESSION.example.md`](../context/SESSION.example.md), [`context/MEMORY.example.md`](../context/MEMORY.example.md) | Runtime state templates for `work.py init-project` | PROMPT_05 | [`docs/runtime-state-workflow.md`](runtime-state-workflow.md) |
