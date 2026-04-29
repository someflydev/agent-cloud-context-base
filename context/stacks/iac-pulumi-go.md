# IaC Pulumi Go

Load this stack for Pulumi programs written in Go. It owns project layout, component types, package boundaries, stack isolation, Automation API usage, and the Go CLI surface.

## Isolation Surface

- Dev stack: `dev`.
- Test stack: `test`.
- Dev env-var prefix: `ACCB_DEV_`.
- Test env-var prefix: `ACCB_TEST_`.
- Dev secret path: `/accb/<repo>/dev/` or provider equivalent.
- Test secret path: `/accb/<repo>/test/` or provider equivalent.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.
- Keep stack config scoped by stack.

## Project Layout

```
infra/pulumi/
  Pulumi.yaml
  Pulumi.dev.yaml
  Pulumi.test.yaml
  go.mod
  go.sum
  main.go
  pkg/components/
  cmd/automation/
```

## Module / Resource Skeleton

- Keep `main.go` focused on stack orchestration.
- Put reusable component types in `pkg/components`.
- Define component args as Go structs.
- Embed `pulumi.ResourceState` in custom component types.
- Accept `Environment`, `NamePrefix`, and provider options in args.
- Register outputs with `ctx.RegisterResourceOutputs`.
- Export snake_case outputs.
- Keep provider-specific package imports near the component that needs them.
- Return errors with context from resource constructors.

## Package Discipline

- Pin `github.com/pulumi/pulumi/sdk/v3/go/pulumi`.
- Add provider modules only for selected providers.
- Commit `go.sum`.
- Run `go fmt`.
- Keep helper packages small and provider-aware.

## Secrets

- Store stack secrets with `pulumi config set --secret`.
- Use Pulumi secret outputs for derived sensitive values.
- Do not log config values in constructors.
- Store runtime secrets in provider-native secret stores.
- Pass only secret names or resource IDs to workloads.

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

- Use `github.com/pulumi/pulumi/sdk/v3/go/auto`.
- Place harness commands under `cmd/automation`.
- Select or create the test stack explicitly.
- Run preview before update when drift risk matters.
- Pass stack outputs to tests without exposing secrets.
- Destroy ephemeral test stacks by default.

## Provider Bindings

- AWS uses `github.com/pulumi/pulumi-aws/sdk/v.../go/aws`.
- GCP uses `github.com/pulumi/pulumi-gcp/sdk/v.../go/gcp`.
- Azure uses `github.com/pulumi/pulumi-azure-native/sdk/go/azure`.
- Kubernetes uses `github.com/pulumi/pulumi-kubernetes/sdk/v.../go/kubernetes`.
- Use explicit providers for multi-target programs.

## Validation Gates

- Reference `context/doctrine/pulumi-stack-discipline.md`.
- Go code is formatted.
- Dev and test stack names are explicit.
- Resource names include the stack.
- Automation cannot update the dev stack by accident.

## Anti-Patterns

- Every resource declared in `main.go`.
- Ignored constructor errors.
- Plaintext secret config.
- Outputs exposing credentials.
- Automation harness using the current selected stack.
