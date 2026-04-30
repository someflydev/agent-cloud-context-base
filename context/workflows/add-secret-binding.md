# Add Secret Binding

Use this workflow when binding a secret to a workload through provider identity and a secret store instead of copying secret values into source, environment files, images, or IaC variables.

## Preconditions

- Provider secret store is chosen: AWS Secrets Manager or SSM, GCP Secret Manager, or Azure Key Vault.
- Workload identity and target runtime are known.
- Dev/test secret paths, identities, and resource names are disjoint.

## Sequence

1. Identify the secret name, runtime consumer, and minimum read action required.
2. Author IaC for the secret metadata or reference, with placeholder value handling that does not commit the secret.
3. Grant the workload identity read access scoped to that one secret or path.
4. Wire the workload to read the secret through provider identity or native secret reference.
5. Avoid plain env-var copy/paste unless the platform only exposes a reference through an environment binding.
6. Add a positive test that the workload can read the secret in the target environment.
7. Add a negative test or policy check showing unrelated secrets are not readable.
8. Verify logs, errors, and test output do not expose the secret value.
9. Update manifest or `.accb/` profile data when the secret binding becomes part of the repo contract.

## Outputs

- Secret metadata/reference, identity policy, workload binding, and positive/negative secret access checks.

## Validation Gates

- `secret-binding-via-identity` from `profile-rules.json`
- `secret-not-in-source`
- `identity-least-privilege-declared`

## Related Docs

- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/stacks/secrets-aws-secrets-manager.md`

## Common Pitfalls

- Storing secret values in Terraform variables, Pulumi config without secret marking, or container images.
- Granting wildcard read over the whole secret store.
- Logging the loaded secret during runtime verification.
