# Cloud Iac Only Repo

Use this archetype for a platform-team repository that contains Terraform modules, Pulumi component resources, environment stacks, policies, and validation but no application runtime code. It is appropriate when the deliverable is reusable cloud infrastructure with explicit dev/test isolation rather than a generated service.

## Common Goals

- Publish reusable infrastructure modules or components with narrow inputs.
- Keep provider and region assumptions explicit and overrideable.
- Provide dev and test stacks that prove module behavior.
- Validate state backend, secret path, and resource-name isolation.
- Keep examples minimal and focused on infrastructure contracts.

## Required Context

- `context/doctrine/iac-dev-test-isolation.md`
- `context/doctrine/terraform-workspace-discipline.md`
- `context/doctrine/pulumi-stack-discipline.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/naming-and-clarity.md`
- the dominant IaC stack pack
- one canonical example from `examples/canonical-iac/`

## Common Workflows

- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-cloud-smoke-tests.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/iac-terraform-aws.yaml`
- `manifests/iac-terraform-gcp.yaml`
- `manifests/iac-terraform-azure.yaml`
- `manifests/iac-pulumi-typescript.yaml`
- `manifests/iac-pulumi-python.yaml`
- `manifests/iac-pulumi-go.yaml`
- `manifests/iac-pulumi-dotnet.yaml`

## Likely Examples

- `examples/canonical-iac/terraform-aws-dev-test-module/`
- `examples/canonical-iac/pulumi-gcp-component-dev-test/`
- `examples/canonical-iac/terraform-azure-platform-catalog/`

## Typical Anti-Patterns

- Leaking application-specific opinions into module defaults.
- Forcing a specific provider region inside a reusable module.
- Sharing backend state keys between dev and test examples.
- Committing tfvars or Pulumi config values that contain secrets.
- Adding application code and still calling the repo IaC-only.

## Validation Gates (summary)

- iac-plan-clean: Terraform plan or Pulumi preview is clean for dev and test.
- iac-dev-test-disjoint: State backend keys, secret paths, env prefixes, and resource names are disjoint.
- secret-not-in-source: No secret values appear in source or IaC config.
- identity-least-privilege-declared: Module-created identities are least privilege by default.
