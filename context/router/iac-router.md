# IaC Router

The IaC router decides whether cloud infrastructure should be represented with Terraform or one Pulumi language. It does not decide provider, runtime tier, application language, or archetype, but it may use those signals to choose a default when the user and repo do not specify an IaC tool.

## Core Rule

Use the explicit IaC tool when named; otherwise choose exactly one tool from repo signals or primary-language affinity, and never emit Terraform and Pulumi for the same non-comparative task.

## Mappings / Signals

- "terraform"
  - load `context/stacks/iac-terraform-conventions.md`
  - load provider stack `context/stacks/iac-terraform-aws.md`, `context/stacks/iac-terraform-gcp.md`, or `context/stacks/iac-terraform-azure.md`
- `*.tf`, `terraform/`
  - load `context/stacks/iac-terraform-conventions.md`
  - load provider stack `context/stacks/iac-terraform-aws.md`, `context/stacks/iac-terraform-gcp.md`, or `context/stacks/iac-terraform-azure.md`
- "pulumi typescript", "pulumi ts", "pulumi node"
  - load `context/stacks/iac-pulumi-typescript.md`
- "pulumi python", "pulumi py"
  - load `context/stacks/iac-pulumi-python.md`
- "pulumi go", "pulumi golang"
  - load `context/stacks/iac-pulumi-go.md`
- "pulumi dotnet", "pulumi csharp", "pulumi c#"
  - load `context/stacks/iac-pulumi-dotnet.md`
- `Pulumi.yaml`, `Pulumi.dev.yaml`, `index.ts` with Pulumi imports, `package.json` with `@pulumi`
  - load `context/stacks/iac-pulumi-typescript.md`
- `Pulumi.yaml`, `Pulumi.dev.yaml`, `__main__.py` with pulumi imports, `requirements.txt` with `pulumi`
  - load `context/stacks/iac-pulumi-python.md`
- `Pulumi.yaml`, `Pulumi.dev.yaml`, `main.go` with Pulumi imports, `go.mod` with `github.com/pulumi/pulumi`
  - load `context/stacks/iac-pulumi-go.md`
- `Pulumi.yaml`, `Pulumi.dev.yaml`, `Program.cs` with Pulumi, `*.csproj` with Pulumi
  - load `context/stacks/iac-pulumi-dotnet.md`
- function or managed-container language python with no IaC tool specified
  - default `pulumi-python`
  - load `context/stacks/iac-pulumi-python.md`
- function or managed-container language typescript or node with no IaC tool specified
  - default `pulumi-typescript`
  - load `context/stacks/iac-pulumi-typescript.md`
- function or managed-container language go with no IaC tool specified
  - default `pulumi-go`
  - load `context/stacks/iac-pulumi-go.md`
- function or managed-container language dotnet with no IaC tool specified
  - default `pulumi-dotnet`
  - load `context/stacks/iac-pulumi-dotnet.md`
- function or managed-container language java or kotlin with no IaC tool specified
  - default `terraform`
  - load `context/stacks/iac-terraform-conventions.md`

## Stop Conditions

- Stop when Terraform and Pulumi are both signaled with no comparative intent.
- Stop when Pulumi is signaled but the Pulumi language cannot be inferred from user language or repo files.
- Stop when provider is unknown and the selected Terraform stack would need provider-specific state, naming, or identity.
- Stop when dev/test state keys, secret paths, and resource naming are undefined for resource generation.

## Routing Examples

- "set up terraform for dev and test on AWS" -> `context/stacks/iac-terraform-conventions.md` + `context/stacks/iac-terraform-aws.md`
- "Pulumi Python stack for a Cloud Run service" -> `context/stacks/iac-pulumi-python.md`
- "Go Lambda repo with no IaC preference" -> `context/stacks/iac-pulumi-go.md`
- "Java service with IaC unspecified" -> `context/stacks/iac-terraform-conventions.md`

