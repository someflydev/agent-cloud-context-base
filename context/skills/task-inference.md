# Task Inference

Use this skill to translate user free-text into a routed `accb` task when the request is vague, business-shaped, or written in aliases. It resolves ambiguity by extracting verbs and nouns, normalizing aliases, routing through task-router, and asking only when workflows tie.

## Procedure

1. Extract action verbs such as add, build, refactor, fix, deploy, bind, wire, test, promote, or generate.
2. Extract nouns such as function, container, k8s role, secret, event, queue, storage, database, identity, observability, or scenario.
3. Normalize provider, runtime tier, language, and IaC aliases through `context/router/alias-catalog.yaml`.
4. Run provider, runtime, IaC, stack, archetype, scenario, and task routers as needed for the noun and verb set.
5. Identify the smallest workflow or workflow chain that can execute the requested action.
6. Preserve explicit constraints from the user even when scenario inference suggests defaults.
7. If multiple workflows tie, name the tied workflows and ask the user to choose.
8. Stop when required dev/test isolation details are missing for cloud resource generation.
9. Record inferred assumptions separately from explicit facts.
10. Pass the routed task into context-bundle assembly.

## Good Triggers

- "what is the user asking for?"
- "route this task"
- "free-text prompt"
- "aliases"
- "which workflow applies?"
- "business prompt to cloud task"

## Avoid

- jumping straight to implementation from ambiguous nouns
- ignoring alias-catalog normalization
- treating scenario inference as stronger than explicit user constraints
- loading workflows before the task action is clear
- guessing between tied workflows without naming the ambiguity
