# Secrets Azure Key Vault

Load this stack for Azure Key Vault secrets in accb-derived repos. It owns vault boundaries, managed identity binding, RBAC and access-policy choices, application secret references, rotation, and validation.

## Capability Surface

- Primary store: Azure Key Vault.
- Dev secret prefix: `<repo>-dev-`.
- Test secret prefix: `<repo>-test-`.
- Dev env-var prefix: `ACCB_DEV_AZURE_`.
- Test env-var prefix: `ACCB_TEST_AZURE_`.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.
- Use one vault per environment when isolation requirements are strict.
- Reference `context/doctrine/cloud-secret-handling.md`.

## Storage Pattern

- Store credentials, tokens, connection strings, and certificates in Key Vault.
- Enable soft delete and purge protection when the platform requires it.
- Use environment-specific vaults or secret names.
- Tag secrets with project, environment, owner, and rotation owner.
- Keep values out of Terraform variables and Pulumi plain config.
- Pass vault URI and secret names to workloads.

## Managed Identity Binding

- Bind Function Apps, Container Apps, AKS workloads, and other compute through managed identity.
- Prefer user-assigned identities when multiple resources need the same identity lifecycle.
- Use system-assigned identity for a single-resource boundary.
- Avoid client secrets for Azure-hosted workloads.
- Keep dev and test managed identities separate.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## RBAC Versus Access Policies

- Prefer Azure RBAC for new vaults when the platform standard supports it.
- Use access policies only when inherited constraints require them.
- Scope `Key Vault Secrets User` or equivalent roles to the vault or secret.
- Avoid subscription-wide secret access.
- Treat portal changes as drift.

## App References

- Azure Functions may use Key Vault references in app settings.
- Container Apps may reference Key Vault secrets through managed identity.
- App Configuration may store Key Vault references when configuration layering is needed.
- Pin secret versions for deterministic tests.
- Use unversioned references only when rotation reload behavior is tested.

## Rotation

- Define rotation owner and cadence.
- Use Event Grid notifications for secret near-expiry when applicable.
- Update new secret versions without exposing values in logs.
- Smoke test workloads after rotation.
- Retire old versions after the recovery window.

## CLI Surface

```bash
az keyvault secret show --vault-name <vault> --name <repo>-dev-<secret>
az keyvault secret set --vault-name <vault> --name <repo>-test-<secret> --value <value>
az role assignment list --assignee <principal-id> --scope <vault-id>
```

## Validation Gates

- Dev and test identities differ.
- Secret names or vaults include environment.
- Workload identity has only required secret read access.
- Key Vault references do not expose plaintext values.
- Rotation owner is documented.

## Anti-Patterns

- Plain application settings containing secret values.
- Shared vault secrets for dev and test.
- Broad Contributor role for secret reads.
- Client secrets stored in source.
- Logging Key Vault payloads.
