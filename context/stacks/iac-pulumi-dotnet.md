# IaC Pulumi Dotnet

Load this stack for Pulumi programs written in .NET. It owns C# and F# project layout, ComponentResource classes, .NET 8 runtime expectations, stack isolation, Automation API usage, and the CLI surface.

## Isolation Surface

- Dev stack: `dev`.
- Test stack: `test`.
- Dev env-var prefix: `ACCB_DEV_`.
- Test env-var prefix: `ACCB_TEST_`.
- Dev secret path: `/accb/<repo>/dev/` or provider equivalent.
- Test secret path: `/accb/<repo>/test/` or provider equivalent.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.
- Keep stack config files separate.

## Project Layout

```
infra/pulumi/
  Pulumi.yaml
  Pulumi.dev.yaml
  Pulumi.test.yaml
  Accb.Infrastructure.csproj
  Program.cs
  Components/
    WorkloadComponent.cs
    NetworkComponent.cs
```

## Module / Resource Skeleton

- Use .NET 8.
- Keep `Program.cs` focused on stack orchestration.
- Create `ComponentResource` classes for reusable bundles.
- Define args classes for component inputs.
- Accept `Environment`, `NamePrefix`, and provider handles.
- Call `RegisterOutputs`.
- Export snake_case outputs through stack dictionaries.
- Use `Output.CreateSecret` for derived sensitive values.
- Keep F# projects parallel when selected by the operator.

## Package Discipline

- Pin `Pulumi`.
- Add `Pulumi.Aws`, `Pulumi.Gcp`, or `Pulumi.AzureNative` as needed.
- Keep the project file minimal.
- Use nullable reference types.
- Run `dotnet format` when available in the generated repo.

## Secrets

- Store stack secrets with `pulumi config set --secret`.
- Do not store plaintext secrets in `Pulumi.<stack>.yaml`.
- Store runtime secrets in provider-native secret stores.
- Pass secret names or resource IDs into applications.
- Keep dev and test secret paths disjoint.

## CLI Surface

```bash
pulumi stack select dev
pulumi preview --stack dev
pulumi up --stack dev
pulumi stack select test
pulumi preview --stack test
pulumi up --stack test
pulumi destroy --stack test
```

## Automation API

- Use `Pulumi.Automation`.
- Put harness code in a separate console project when needed.
- Select or create the test stack explicitly.
- Run preview before update when drift risk matters.
- Return non-secret outputs to integration tests.
- Destroy ephemeral test stacks by default.

## Provider Bindings

- AWS uses `Pulumi.Aws`.
- GCP uses `Pulumi.Gcp`.
- Azure uses `Pulumi.AzureNative`.
- Kubernetes uses `Pulumi.Kubernetes`.
- Use explicit providers when multiple subscriptions, projects, accounts, or clusters are active.

## Validation Gates

- Reference `context/doctrine/pulumi-stack-discipline.md`.
- Project targets .NET 8.
- Dev and test stack files exist.
- Resource names include the stack.
- Automation uses the test stack only.

## Anti-Patterns

- Resource sprawl in `Program.cs`.
- Plain config for secret values.
- Component resources without registered outputs.
- Outputs exposing credentials.
- Automation API relying on the selected current stack.
