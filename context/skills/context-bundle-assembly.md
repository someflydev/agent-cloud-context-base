# Context Bundle Assembly

Use this skill to assemble the first-pass context bundle from router output and the chosen manifest. It resolves ambiguity by intersecting required context with the task surface, applying the complexity budget, and emitting a justified load order.

## Procedure

1. Run the seven routers: provider, runtime, IaC, stack, archetype, scenario, and task.
2. Identify the chosen manifest or stop and use manifest selection when candidates tie.
3. List the manifest's required and optional context items.
4. Intersect router output with required manifest context first.
5. Add optional context only when it directly supports the active task surface.
6. Apply the complexity-budget cap from cloud context-loading doctrine.
7. Use load order: doctrine, router notes, workflow, stack, archetype, manifest, canonical example.
8. Load one primary workflow, one primary runtime stack, one IaC stack, and one example unless the task has clear orthogonal concerns.
9. Stop when two workflows, stacks, or examples tie and no signal breaks the tie.
10. Emit the approved bundle with required versus optional items labeled.

## Good Triggers

- "what should I load?"
- "assemble the context bundle"
- "router output plus manifest"
- "required versus optional context"
- "complexity budget"
- "first-pass bundle"

## Avoid

- loading whole directories because the task is broad
- treating optional manifest context as automatically required
- loading multiple near-match examples as a hedge
- skipping routers and selecting files by intuition
- widening the bundle instead of stopping on unresolved ambiguity
