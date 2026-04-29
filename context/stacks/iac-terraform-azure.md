# IaC Terraform Azure

Load this stack for Terraform-managed Azure infrastructure in accb-derived repos. It owns azurerm provider configuration, AzureRM remote state, subscription and resource-group hierarchy, common modules, and role assignments.

## Isolation Surface

- Dev state: blob key `accb/<repo>/dev/terraform.tfstate`.
- Test state: blob key `accb/<repo>/test/terraform.tfstate`.
- Locking: Azure Blob lease on the state blob.
- Dev env-var prefix: `ACCB_DEV_AZURE_`.
- Test env-var prefix: `ACCB_TEST_AZURE_`.
- Dev secret path: Key Vault secret prefix `<repo>-dev-`.
- Test secret path: Key Vault secret prefix `<repo>-test-`.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.

## Provider Configuration

- Use pinned `hashicorp/azurerm`.
- Set `features {}` explicitly.
- Require `subscription_id`, `tenant_id`, `location`, and `environment`.
- Use provider aliases for multiple subscriptions.
- Apply tags for `project`, `environment`, `managed_by`, and `repo`.
- Avoid developer CLI login as the generated automation credential.

## Remote State

- Use the AzureRM backend with a storage account and container.
- Rely on blob lease state locking.
- Enable storage account soft delete and versioning when available.
- Use separate blob keys for dev and test.
- Restrict state storage network access when the platform requires it.
- Bootstrap state storage before workload modules.

## Hierarchy Pattern

- Keep subscription ownership explicit.
- Use one resource group per environment and workload slice unless the manifest chooses otherwise.
- Put shared networking in a declared shared resource group.
- Keep role assignments in Terraform.
- Treat portal-created role assignments as drift.

## Module / Resource Skeleton

```
modules/vnet/
modules/aks/
modules/function-app/
modules/container-app/
modules/key-vault/
modules/role-assignment/
```

- Each module accepts `environment`, `name_prefix`, `location`, and `tags`.
- VNet modules output subnet IDs and private DNS link data.
- AKS modules output kubeconfig metadata without secrets.
- Function and Container Apps modules accept managed identity IDs.
- Key Vault modules output vault ID and URI.
- Role-assignment modules scope principal permissions tightly.

## Identity Pattern

- Prefer managed identities for workloads.
- Use user-assigned managed identities when identity reuse is deliberate.
- Use system-assigned identities for single-resource lifecycles.
- Assign RBAC roles at resource or resource-group scope.
- Avoid subscription-wide role assignments without a manifest waiver.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## CLI Surface

```bash
terraform init -backend-config=backend-dev.hcl
terraform plan -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
terraform init -reconfigure -backend-config=backend-test.hcl
terraform plan -var-file=env/test.tfvars
terraform destroy -var-file=env/test.tfvars
```

## Common Resources

- Virtual networks and subnets.
- AKS clusters with workload identity.
- Function Apps with managed identity.
- Container Apps and environments.
- Key Vault with RBAC or access policies.
- Role assignments scoped to resource boundaries.

## Validation Gates

- Blob state keys differ by environment.
- Resource groups include the environment name.
- Managed identities differ for dev and test.
- Key Vault access is identity-based.
- Plans target only the expected subscription.

## Anti-Patterns

- Contributor at subscription scope for workloads.
- One resource group with mixed dev and test resources.
- Key Vault secrets copied into tfvars.
- Portal-only role assignments.
- State storage exposed broadly.
