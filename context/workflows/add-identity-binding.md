# Add Identity Binding

Use this workflow when creating or modifying an IAM role, service account, managed identity, or workload identity binding for a workload and a bounded set of resources.

## Preconditions

- Workload, provider identity system, target resources, and required actions are known.
- Dev/test identities and resource scopes are disjoint.
- The access need cannot be met by an existing narrower binding.

## Sequence

1. Identify the smallest action set the workload needs.
2. Identify resource ARNs, names, paths, or scopes for each allowed action.
3. Author IaC for the role, service account, managed identity, or federation binding.
4. Bind the identity to the workload deployment or function.
5. Add policy statements scoped to exact resources where the provider supports it.
6. Avoid wildcard actions and cross-environment resource patterns.
7. Add a positive test proving an allowed action succeeds.
8. Add a negative test proving a disallowed action fails with a 403 or provider equivalent.
9. Run plan/preview and update manifest profile data when identity is part of the contract.

## Outputs

- Identity resource, workload binding, scoped policy, and positive/negative access checks.

## Validation Gates

- `identity-least-privilege-declared` from `profile-rules.json`
- `iac-dev-test-disjoint`
- `changed-boundary-proof`

## Related Docs

- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/stacks/identity-gcp-iam-sa.md`

## Common Pitfalls

- Sharing one identity across unrelated workload roles.
- Using wildcard resources because exact names are not yet known.
- Proving only that allowed access works while never checking denied access.
