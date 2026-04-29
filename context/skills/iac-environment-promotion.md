# IaC Environment Promotion

Use this skill to decide what changes between dev and test infrastructure stacks or workspaces. It resolves ambiguity by making state, secrets, naming, regions, identities, and shared inputs explicit before promotion or resource generation.

## Procedure

1. List every per-environment axis: state backend, state key or stack name, secret path, env-var prefix, resource names, region, account or project, and identity.
2. Confirm whether dev and test use separate accounts/projects/subscriptions or separate names inside one boundary.
3. Define disjoint state: Terraform backend keys or Pulumi stacks must not be shared.
4. Define disjoint secret paths and environment-specific KMS keys or aliases when keys are declared.
5. Define deterministic resource naming with environment suffixes for all referenced resources.
6. Define separate workload identities and scoped permissions for each environment.
7. Identify dev-only inputs, test-only inputs, and shared read-only inputs.
8. Produce the dev config and test config side by side so differences are auditable.
9. Require explicit operator opt-in before persistent test resources are retained.
10. Stop when any cloud resource would be generated without the isolation surface declared.

## Good Triggers

- "promote dev to test"
- "dev/test isolation"
- "Terraform workspace"
- "Pulumi stacks"
- "separate state"
- "test resources keep colliding with dev"

## Avoid

- sharing state files or stack config across dev and test
- using the same secret path for both environments
- relying on provider-generated names for referenced resources
- granting identities permissions across both environments
- treating region, account, project, or subscription differences as incidental
