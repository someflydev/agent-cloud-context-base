# IaC Terraform GCP

Load this stack for Terraform-managed Google Cloud infrastructure in accb-derived repos. It owns google provider configuration, GCS state, project hierarchy, common modules, and service-account boundaries.

## Isolation Surface

- Dev state: GCS object `accb/<repo>/dev/terraform.tfstate`.
- Test state: GCS object `accb/<repo>/test/terraform.tfstate`.
- Dev env-var prefix: `ACCB_DEV_GCP_`.
- Test env-var prefix: `ACCB_TEST_GCP_`.
- Dev secret path: `projects/<project>/secrets/<repo>-dev-*`.
- Test secret path: `projects/<project>/secrets/<repo>-test-*`.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.
- Use separate projects when the operator chooses strong isolation.

## Provider Configuration

- Use pinned `hashicorp/google` and `hashicorp/google-beta` providers.
- Require explicit `project`, `region`, and `environment` variables.
- Use provider aliases for multiple projects or folders.
- Keep beta resources behind a visible module boundary.
- Apply labels for `project`, `environment`, `managed_by`, and `repo`.
- Avoid implicit Application Default Credentials in CI.

## Remote State

- Use a GCS backend bucket with Object Versioning.
- Enable uniform bucket-level access.
- Encrypt state with a CMEK when the platform requires it.
- Use separate state prefixes for dev and test.
- Bootstrap state storage before workload modules.
- Keep state bucket IAM narrower than deployment IAM.

## Hierarchy Pattern

- Model folder and project ownership explicitly when generated.
- Keep dev and test projects separate when quota or IAM boundaries require it.
- Use Shared VPC only when the network host project is declared.
- Track enabled APIs in Terraform.
- Keep billing account attachment out of examples unless the operator opts in.

## Module / Resource Skeleton

```
modules/network/
modules/gke/
modules/cloudfunctions2/
modules/cloudrun/
modules/service-account/
```

- Each module accepts `environment`, `name_prefix`, `project_id`, and `labels`.
- Network modules output VPC, subnet, and connector identifiers.
- GKE modules output cluster endpoint and workload identity pool data.
- Cloud Run and Cloud Functions modules accept service account emails.
- Service-account modules output email, name, and minimal binding handles.

## Identity Pattern

- Use one service account per workload boundary.
- Grant roles at resource scope when possible.
- Use project-level bindings only when APIs require it.
- Avoid primitive Owner, Editor, and Viewer roles.
- Use IAM conditions where the resource supports them.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

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

- VPC networks and subnets.
- GKE clusters with Workload Identity.
- Cloud Functions v2 services.
- Cloud Run services and jobs.
- Secret Manager secrets and versions.
- Service accounts with scoped IAM bindings.

## Validation Gates

- Required APIs are declared.
- State bucket has Object Versioning.
- Dev and test state prefixes differ.
- Service accounts include the environment suffix.
- Plans target only the expected project and region.

## Anti-Patterns

- Editor role for deployment or workload identities.
- State bucket without versioning.
- Hard-coded default project in modules.
- Shared service account for dev and test.
- Beta provider use hidden in root resources.
