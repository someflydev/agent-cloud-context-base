# Refresh Mermaid Diagrams

Use this workflow when updating Mermaid diagrams to match current architecture, routing, workflow, or cloud boundary docs.

## Preconditions

- Source docs or code that define the diagrammed behavior have been inspected.
- The diagram update is scoped to Mermaid text, adjacent labels, or references.
- Cloud resource semantics are not invented just to make the diagram simpler.

## Sequence

1. Identify the diagram source file and the behavior it represents.
2. Compare the diagram against current router, archetype, stack, workflow, or IaC docs.
3. Update nodes and edges to reflect actual current files and resource boundaries.
4. Keep provider-specific labels clear when multiple providers are shown.
5. Avoid decorative detail that makes the diagram harder to maintain.
6. Validate Mermaid syntax with the repo's available docs command when present.
7. Check that all referenced workflow, stack, manifest, or example paths exist.
8. Update nearby prose only when it contradicts the refreshed diagram.
9. Record skipped rendering validation as `incomplete` if no renderer is available.

## Outputs

- Mermaid diagrams that match current repo behavior and valid references.

## Validation Gates

- `startup-rehydration` from `profile-rules.json`
- `changed-boundary-proof`

## Related Docs

- `context/doctrine/documentation-timing-discipline.md`
- `context/doctrine/naming-and-clarity.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Updating a diagram from memory instead of current files.
- Referencing future manifests or workflows that do not exist yet.
- Making diagrams provider-neutral where provider behavior is the point.
