# Documentation Timing Discipline

Documentation should describe real behavior rather than predicted architecture. The base repo documents its operating system fully, while generated cloud repos earn front-facing prose as implementation becomes concrete.

## Keep Derived Repos Lean

- Start generated repos with minimal root README content.
- Avoid substantial root `docs/` content before implementation has shape.
- Avoid Mermaid architecture diagrams before resources, boundaries, and flows are known.
- Keep day-one prose focused on how to run, verify, and continue work.
- Prefer manifests and validation contracts over speculative narrative.

## Document After Substance

- Add architecture prose after handlers, services, workloads, and IaC exist.
- Describe actual triggers, routes, queues, topics, jobs, and clusters.
- Include deployed resource names only when they are deterministic and non-secret.
- Tie diagrams to verified runtime topology.
- Update docs when implementation changes the boundary.

## Treat Base Docs Differently

- Document `accb` fully because its job is to guide generated repos.
- Keep doctrine, workflows, stacks, archetypes, examples, templates, and validation discoverable.
- Explain prompt sequence decisions in base documentation when they affect later work.
- Keep generated `.accb/` payload rules clear.
- Avoid hiding core behavior in session notes only.

## Use Placeholders Carefully

- Keep `templates/readme/` placeholders explicit about when to fill them.
- Avoid polished marketing copy in new generated repos.
- Avoid claims about reliability, scale, or security before verification exists.
- Leave TODOs only when a later prompt or operator action owns them.
- Remove stale placeholders once real docs land.

## Keep Docs Verifiable

- Pair operational docs with commands that still work.
- Pair architecture docs with IaC or manifests that define the resources.
- Treat screenshots and diagrams as secondary to runnable proof.
- Mark docs incomplete when implementation is not ready to support them.
- Validate documentation timing as part of repo generation review.
