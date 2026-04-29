# Identity Azure Entra Managed Identity

Load this stack for Azure identity in accb-derived repos. It owns Entra ID concepts, system-assigned and user-assigned managed identities, RBAC role assignments, AKS Workload Identity, federated credentials, and conditional access awareness.

## Capability Surface

- Workload identity: managed identity.
- Directory layer: Microsoft Entra ID.
- AKS identity: Workload Identity with federated credentials.
- Dev identity names: `<repo>-dev-<workload>-mi`.
- Test identity names: `<repo>-test-<workload>-mi`.
- Dev env-var prefix: `ACCB_DEV_AZURE_`.
- Test env-var prefix: `ACCB_TEST_AZURE_`.
- Reference `context/doctrine/identity-and-least-privilege.md`.

## Managed Identity Pattern

- Use system-assigned identities for single-resource lifecycles.
- Use user-assigned identities when identity lifecycle must outlive or span resources.
- Keep deployer identities separate from runtime identities.
- Keep dev and test identities separate.
- Avoid client secrets for Azure-hosted workloads.
- Record principal IDs as non-secret outputs.

## RBAC Pattern

- Assign roles at resource scope where possible.
- Use resource-group scope when a workload truly spans resources.
- Avoid subscription scope unless a manifest waiver exists.
- Prefer data-plane roles over broad management-plane roles.
- Treat Owner and Contributor roles as privileged exceptions.
- Keep role assignments in Terraform or Pulumi.

## AKS Workload Identity

- Enable OIDC issuer and workload identity on the cluster.
- Create federated identity credentials for Kubernetes service accounts.
- Scope subject by namespace and service account.
- Keep namespaces environment-specific.
- Avoid pod-mounted client secrets.
- Validate access from the deployed pod identity.

## Federated Credentials

- Use federated credentials for CI and AKS when available.
- Restrict issuer, subject, and audience.
- Keep deploy federation separate from runtime federation.
- Rotate or remove unused federated credentials.
- Review Entra app permissions when application registrations are used.

## Conditional Access

- Conditional access usually targets human and app sign-ins, not managed identities.
- Document tenant policies that affect deployment identities.
- Avoid bypassing conditional access by creating unmanaged credentials.
- Keep break-glass identities out of generated examples.

## CLI Surface

```bash
az identity show --name <repo>-dev-<workload>-mi --resource-group <rg>
az role assignment list --assignee <principal-id>
az aks show --name <cluster> --resource-group <rg> --query oidcIssuerProfile
```

## Validation Gates

- Dev and test managed identities differ.
- Role assignment scopes are narrow.
- AKS federated credential subjects are exact.
- Client secrets are absent from source and app config.
- Privileged roles have visible waivers.

## Anti-Patterns

- Connection strings instead of managed identity.
- Contributor for every workload.
- Shared identity across unrelated services.
- Portal-created role assignments.
- Federated credentials with broad subjects.
