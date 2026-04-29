# Canonical Examples

Canonical examples reduce cloud ambiguity by showing one verified way to build a complete pattern. They are runnable reference implementations, not decorative snippets or substitutes for templates.

## Define The Cell

- Organize examples by provider, runtime tier, language, and IaC tool.
- Maintain one preferred example per provider, runtime, and language cell.
- Include Terraform for each canonical pattern.
- Include at least one Pulumi-language equivalent for each canonical pattern.
- Provide dev and test stacks for every example that provisions resources.

## Keep Examples Real

- Use complete code that can run.
- Include handler, service, or workload code as appropriate.
- Include IaC, identity, secrets references, observability, and test commands.
- Avoid prose-only examples.
- Avoid partial snippets that require hidden setup.

## Separate Templates From Examples

- Use templates to scaffold new repos.
- Use examples to demonstrate completed cloud patterns.
- Do not make generated repos depend on examples at runtime.
- Do not use examples as a dumping ground for every variant.
- Keep templates lean and examples opinionated.

## Maintain Trust

- Index examples in `examples/catalog.json`.
- Record trust and last-verified state in `verification/example_registry.yaml`.
- Audit affected examples when doctrine changes.
- Mark stale examples instead of letting them imply current guidance.
- Prefer fewer verified examples over many unproven variants.

## Route Honestly

- Route requests to the closest verified example when it fits.
- Say explicitly when no canonical example fits.
- Pair gaps with relevant doctrine and invariants.
- Avoid inventing a hybrid example during task execution.
- Create new examples through the prompt sequence, not ad hoc scope creep.
