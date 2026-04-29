# IaC Terraform Conventions

Load this stack for Terraform in accb-derived repos. It owns repo layout, state isolation, provider pinning, module boundaries, and the CLI surface shared by AWS, GCP, and Azure Terraform stacks.

## Isolation Surface

- Dev state key: `<repo>/dev/terraform.tfstate`.
- Test state key: `<repo>/test/terraform.tfstate`.
- Dev env-var prefix: `ACCB_DEV_`.
- Test env-var prefix: `ACCB_TEST_`.
- Dev secret path prefix: `/accb/<repo>/dev/`.
- Test secret path prefix: `/accb/<repo>/test/`.
- Dev resource naming: `<repo>-dev-<role>`.
- Test resource naming: `<repo>-test-<role>`.
- Never reuse one backend object for both environments.
- Declare backend ownership before generating resources.

## Project Layout

```
infra/terraform/
  versions.tf
  providers.tf
  main.tf
  variables.tf
  outputs.tf
  env/dev.tfvars
  env/test.tfvars
  modules/<name>/main.tf
  modules/<name>/variables.tf
  modules/<name>/outputs.tf
```

## Module / Resource Skeleton

- Put reusable resources under `modules/<x>/`.
- Keep each module to one provider capability boundary.
- Define `environment` as a required string variable.
- Pass `name_prefix` or `resource_prefix` into every module.
- Type every variable and output.
- Mark sensitive outputs as `sensitive = true`.
- Keep provider configuration at the root module.
- Keep data sources close to the resource that consumes them.
- Prefer explicit resource names over provider-generated names.
- Keep lifecycle ignores narrow and justified in comments.

## Provider Discipline

- Pin Terraform with `required_version`.
- Pin every provider with a lower and upper bound.
- Commit `.terraform.lock.hcl` after provider initialization.
- Use provider aliases only when multiple accounts, projects, subscriptions, or regions are intentional.
- Keep default tags or labels centralized when the provider supports them.
- Do not use credentials from local profiles in generated automation without an explicit operator choice.

## CLI Surface

```bash
terraform init -backend-config=backend-dev.hcl
terraform fmt -check -recursive
terraform validate
terraform plan -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
terraform plan -var-file=env/test.tfvars
terraform destroy -var-file=env/test.tfvars
```

## Environment Variables

- Use `var.environment` in every resource name.
- Use `dev.tfvars` for dev inputs.
- Use `test.tfvars` for test inputs.
- Do not share tfvars files across environments.
- Keep secret values out of tfvars.
- Resolve secret names or ARNs through provider-native secret stores.

## Pre-Commit Gates

- Run `terraform fmt -check -recursive`.
- Run `terraform validate`.
- Run a provider-specific static scanner when the generated repo enables one.
- Fail when a module lacks `variables.tf` or `outputs.tf`.
- Fail when dev and test backend keys match.

## Validation Gates

- Reference `context/doctrine/iac-dev-test-isolation.md`.
- Reference `context/doctrine/terraform-workspace-discipline.md`.
- `python3 scripts/validate_iac_isolation.py <path>` must pass after PROMPT_17.
- Plans must show only intended changes before integration tests.

## Anti-Patterns

- One state file for every environment.
- Untyped variables.
- Plaintext secrets in tfvars.
- Provider versions left floating.
- Resources named without an environment suffix.
