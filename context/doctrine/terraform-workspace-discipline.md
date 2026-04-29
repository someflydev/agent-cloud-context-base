# Terraform Workspace Discipline

Terraform isolation must be visible in state, variables, names, and credentials. Workspaces are acceptable only when their state prefixes and operational boundaries remain unambiguous.

## Prefer Separate State

- Use separate backends with distinct keys for dev and test when possible.
- Use separate workspaces with disjoint state prefixes only when separate backends are impractical.
- Never share state files across environments.
- Store backend credentials in a provider secret store.
- Keep state backend configuration documented beside the IaC.

## Separate Variables

- Use `dev.tfvars` for dev.
- Use `test.tfvars` for test.
- Do not share variable files across environments.
- Type module variables explicitly.
- Include `var.environment` in resource naming inputs.

## Name Deterministically

- Include the environment suffix in every resource name.
- Keep buckets, queues, topics, functions, services, and identities distinct across dev and test.
- Use snake_case for outputs.
- Avoid ambiguous abbreviations in user-facing resource names.
- Keep generated names predictable for teardown.

## Plan Before Tests

- Run `terraform plan` before Lane B integration tests.
- Require a clean plan with no unintended drift.
- Stop when plan output includes unrelated changes.
- Destroy ephemeral test resources by default.
- Run IaC isolation validation after Terraform changes.
