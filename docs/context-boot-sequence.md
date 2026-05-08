# Context Boot Sequence

Assistants must start from the smallest useful cloud profile and broaden only when the task proves ambiguity. This keeps provider, runtime tier, language, and IaC decisions explicit.

## Startup Contract

1. Read [`AGENT.md`](../AGENT.md).
2. Run `python3 scripts/work.py resume`.
3. Read [`memory/INDEX.md`](../memory/INDEX.md) and only the concept artifact relevant to the current task.
4. Confirm provider, runtime tier, language, and IaC tool from the user prompt or from `.accb/profile/selection.json` in a generated repo.
5. Load one router, one workflow, one stack pack, one archetype, one scenario pattern, and one canonical example.
6. Refuse to broaden the context bundle until ambiguity is resolved.

## Boot Flow

```mermaid
flowchart TD
    A[Read AGENT.md] --> B[Run work.py resume]
    B --> C[Read memory/INDEX.md]
    C --> D{Profile declared?}
    D -->|prompt gives provider/runtime/language/IaC| E[Use declared profile]
    D -->|generated repo| F[Read .accb/profile/selection.json]
    D -->|ambiguous| G[Ask or route with one router]
    E --> H{Runtime tier}
    F --> H
    G --> H
    H -->|function| I[Load function router/workflow/stack/archetype/scenario/example]
    H -->|managed container| J[Load container router/workflow/stack/archetype/scenario/example]
    H -->|k8s| K[Load Kubernetes router/workflow/stack/archetype/scenario/example]
    I --> L[Declare dev/test isolation surface]
    J --> L
    K --> L
    L --> M[Execute one bounded task]
    M --> N[Validate before done]
```

## Isolation Declaration

Before generating or changing cloud resources, declare the dev/test isolation surface:

- State: separate Terraform backends/workspaces or Pulumi stacks.
- Environment variables: distinct `ACCB_*_DEV_` and `ACCB_*_TEST_` prefixes.
- Secrets: distinct provider secret paths or vault locations.
- Resource naming: environment-suffixed names for managed resources.
