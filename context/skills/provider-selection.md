# Provider Selection

Use this skill to pick AWS, GCP, or Azure when a user prompt is provider-agnostic or contains weak mixed signals. It resolves provider ambiguity by reading repo signals first, respecting declared organizational defaults, and only asking when no provider-native fit dominates.

## Procedure

1. Run the provider router over user language, file paths, imports, IaC files, and service names.
2. Treat explicit provider language as strongest unless the user states a migration or comparative task.
3. Check repo signals such as `provider "aws"`, `google.cloud` imports, `host.json`, `Pulumi.*.yaml`, or provider-specific directories.
4. Ask whether an organizational default exists if repo signals are absent or tied.
5. Compare the workload's needed managed services against provider-native equivalents for storage, database, eventing, identity, secrets, and observability.
6. Prefer the provider whose native service set covers the workload with the fewest semantic gaps.
7. If the prompt names provider-specific services from more than one provider, determine whether the task is comparative, migration, or accidental mixing.
8. Stop and ask when no provider dominates and resource generation would require provider-specific identity, state, naming, or secrets.
9. Record the provider decision with runtime tier, language, IaC tool, and dev/test isolation before generation.

## Good Triggers

- "pick a cloud provider"
- "AWS or GCP or Azure?"
- "provider agnostic prompt"
- "no provider is named"
- "which provider should accb use?"
- "the services are provider-neutral"

## Avoid

- choosing a provider from one weak comment while repo files point elsewhere
- mixing provider services in a non-comparative repo
- ignoring an operator-declared organizational default
- treating managed-service names as interchangeable without checking semantics
- generating provider-specific resources before the provider is resolved
