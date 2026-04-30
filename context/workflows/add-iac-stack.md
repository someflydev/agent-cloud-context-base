# Add IaC Stack

Use this workflow when adding a Terraform or Pulumi stack that owns new cloud resources or a new module/component boundary.

## Preconditions

- IaC tool, provider, target environment names, and resource ownership boundary are chosen.
- Dev/test state backends or Pulumi stacks are declared separately.
- Resource naming, env-var prefixes, secret paths, and identities are planned before resources are authored.

## Sequence

1. Pick the IaC stack pack for Terraform or the selected Pulumi language.
2. Define the module or component boundary and keep ownership narrow.
3. Author dev and test configuration with disjoint state keys or stacks.
4. Apply deterministic resource naming with environment suffixes.
5. Add identity, secret, network, storage, and eventing dependencies as explicit inputs or child resources.
6. Keep provider credentials and secret values out of source.
7. Run formatting and static validation for the chosen IaC tool.
8. Run `terraform plan` or `pulumi preview` cleanly in dev.
9. Repeat the plan or preview for test when the workflow changes shared modules.

## Outputs

- Terraform module/root stack or Pulumi component/stack with dev and test environment configuration.

## Validation Gates

- `iac-plan-clean` from `profile-rules.json`
- `iac-dev-test-disjoint`
- `secret-not-in-source`

## Related Docs

- `context/doctrine/iac-dev-test-isolation.md`
- `context/doctrine/terraform-workspace-discipline.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Sharing one state key and relying only on variable differences.
- Leaving provider-generated names for resources referenced by other systems.
- Hiding identity or secret dependencies in application configuration.
