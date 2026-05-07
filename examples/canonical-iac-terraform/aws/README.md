# Canonical Terraform IaC: AWS

This starter isolates `dev` and `test` AWS surfaces for an `.accb/` generated
repo. It contains no application code; it only models the reusable platform
shape used by canonical function, container, and k8s examples.

Isolation contract:

- State: `dev/backend.tf` and `test/backend.tf` use different S3 backend keys.
- Env prefix: modules accept `var.environment` and suffix or prefix resource names.
- Secrets: secret names are environment-scoped, for example `accb/dev/app/config`.
- Resources: names include `accb-${var.environment}`.

Run:

```sh
terraform -chdir=dev init
terraform -chdir=dev plan -var-file=dev.tfvars
terraform -chdir=test init
terraform -chdir=test plan -var-file=test.tfvars
python3 scripts/validate_iac_isolation.py examples/canonical-iac-terraform/aws
```
