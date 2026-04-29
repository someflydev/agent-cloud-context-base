# Archetype Router

The archetype router decides the generated repository shape to load from `context/archetypes/` once the workload topology is understood. It does not choose provider, runtime tier, language, IaC tool, or scenario; it maps the intended repo organization and operating boundary.

## Core Rule

Choose the archetype that matches the repository's durable workload shape, not a single implementation task inside that repository.

## Mappings / Signals

- "single function with iac"
  - load `context/archetypes/cloud-function-repo.md`
- "platform with multiple functions"
  - load `context/archetypes/multi-function-platform.md`
- "single managed-container service"
  - load `context/archetypes/managed-container-service.md`
- "primary api + private worker + jobs"
  - load `context/archetypes/managed-container-multi-service.md`
- "k8s api + workers + jobs + crons"
  - load `context/archetypes/k8s-platform-repo.md`
- "k8s tenant per namespace"
  - load `context/archetypes/k8s-multi-tenant-platform.md`
- "trigger -> enrich -> persist -> fan-out"
  - load `context/archetypes/cloud-event-pipeline.md`
- "cloud-side data acquisition"
  - load `context/archetypes/cloud-data-acquisition.md`
- "rag pipeline with embeddings + vector"
  - load `context/archetypes/cloud-rag-pipeline.md`
- "thin orchestrator over heavy compute"
  - load `context/archetypes/cloud-control-plane.md`
- "iac catalog only repo"
  - load `context/archetypes/cloud-iac-only-repo.md`
- "compare aws vs gcp vs azure for x"
  - load `context/archetypes/cloud-multi-provider-experiment.md`

## Stop Conditions

- Stop when a request only describes an implementation task and not enough repo shape exists to choose an archetype.
- Stop when two archetypes imply different runtime tiers and the runtime router has not resolved the tier.
- Stop when the user asks for an IaC-only repo but also asks for runtime code without saying whether to include examples.
- Stop when a comparative archetype is implied by mixed providers but the user has not declared comparative intent.

## Routing Examples

- "single Lambda with Terraform" -> `context/archetypes/cloud-function-repo.md`
- "claims intake API with private worker and nightly job" -> `context/archetypes/managed-container-multi-service.md`
- "k8s tenant per namespace platform" -> `context/archetypes/k8s-multi-tenant-platform.md`
- "compare AWS vs GCP vs Azure for object upload enrichment" -> `context/archetypes/cloud-multi-provider-experiment.md`

