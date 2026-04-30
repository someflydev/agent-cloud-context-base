# Add IaC Isolation Pair

Use this workflow when adding or repairing the paired dev and test isolation surface for an existing IaC stack.

## Preconditions

- Existing Terraform or Pulumi stack boundary is known.
- Dev and test environments both need explicit isolation.
- The repo can run `python3 scripts/validate_iac_isolation.py <path>` after PROMPT_17.

## Sequence

1. Locate every state backend key, workspace, Pulumi stack, config file, and provider variable involved in the stack.
2. Declare disjoint dev and test state backend keys or Pulumi stack names.
3. Declare disjoint env-var prefixes for application and IaC configuration.
4. Declare disjoint secret paths and KMS/key references when secrets are present.
5. Declare resource names with deterministic dev and test suffixes.
6. Declare separate workload identities or service accounts for dev and test.
7. Update validation fixtures or manifests so the isolation surface is machine-checkable.
8. Run IaC format and plan/preview for both environments.
9. Run `python3 scripts/validate_iac_isolation.py <path>`.

## Outputs

- Dev/test IaC configuration pair with separate state, names, secrets, env vars, and identities.

## Validation Gates

- `iac-dev-test-disjoint` from `profile-rules.json`
- `iac-plan-clean`
- `identity-least-privilege-declared`

## Related Docs

- `context/doctrine/iac-dev-test-isolation.md`
- `context/doctrine/multi-environment-promotion.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Considering workspaces enough while backend keys remain ambiguous.
- Reusing one secret path with environment-specific values.
- Letting one identity access both dev and test resources.
