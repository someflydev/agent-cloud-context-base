# IaC Terraform AWS

Load this stack for Terraform-managed AWS infrastructure in accb-derived repos. It owns AWS provider configuration, remote state, common modules, IAM boundaries, and AWS-specific CLI expectations.

## Isolation Surface

- Dev state: S3 key `accb/<repo>/dev/terraform.tfstate`.
- Test state: S3 key `accb/<repo>/test/terraform.tfstate`.
- State lock: DynamoDB table with environment-scoped lock records.
- Dev env-var prefix: `ACCB_DEV_AWS_`.
- Test env-var prefix: `ACCB_TEST_AWS_`.
- Dev secret path: `/accb/<repo>/dev/`.
- Test secret path: `/accb/<repo>/test/`.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.

## Provider Configuration

- Use `hashicorp/aws` with a pinned version.
- Require an explicit `region` variable.
- Use `assume_role` for deployment roles when cross-account deployment is active.
- Keep dev and test deployment roles separate when accounts are shared.
- Set default tags in the provider block.
- Include `Project`, `Environment`, `ManagedBy`, and `Repo` tags.
- Avoid local named profiles in generated CI commands.

## Remote State

- Use an S3 backend with bucket versioning enabled.
- Encrypt state with SSE-KMS when a KMS key is declared.
- Use DynamoDB locking.
- Keep bucket names globally unique and environment-aware.
- Do not place dev and test under the same key.
- Document backend bootstrap separately from workload modules.

## Module / Resource Skeleton

```
modules/vpc/
modules/eks/
modules/s3-bucket/
modules/lambda/
modules/iam-role/
```

- Each module accepts `environment`, `name_prefix`, and `tags`.
- Each module emits only non-secret outputs needed by callers.
- Network modules output subnet IDs, route table IDs, and security group IDs.
- Compute modules accept role ARNs rather than creating broad roles inline.
- Storage modules expose ARNs for least-privilege policy attachment.

## IAM Pattern

- Use one IAM role per workload boundary.
- Build policies from exact action and resource lists.
- Attach permission boundaries when the organization requires them.
- Use condition keys for source account, source ARN, VPC endpoint, or principal tags when useful.
- Keep KMS decrypt permission separate from service permissions.
- Reference `context/stacks/identity-aws-iam.md`.

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

- VPC with public, private, and isolated subnet tiers when needed.
- EKS with managed node groups and IRSA.
- S3 buckets with encryption, public access block, versioning, and lifecycle.
- Lambda functions with dedicated execution roles.
- IAM roles with scoped inline policies.
- KMS keys with aliases per environment when encryption is managed.

## Validation Gates

- Backend bucket versioning is enabled.
- DynamoDB lock table exists before shared applies.
- Default tags include environment.
- Dev and test role ARNs differ.
- Plans do not mutate unrelated accounts or regions.

## Anti-Patterns

- Sharing one admin role across all workloads.
- S3 state without locking.
- Wildcard `iam:*` policies.
- Buckets without public access block.
- Region implied only by a developer shell.
