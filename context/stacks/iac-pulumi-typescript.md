# IaC Pulumi TypeScript

Load this stack for Pulumi programs written in TypeScript. It owns project layout, component resources, config secrets, stack isolation, Automation API usage, and the TypeScript CLI surface.

## Isolation Surface

- Dev stack: `dev`.
- Test stack: `test`.
- Dev env-var prefix: `ACCB_DEV_`.
- Test env-var prefix: `ACCB_TEST_`.
- Dev secret path: `/accb/<repo>/dev/` or provider equivalent.
- Test secret path: `/accb/<repo>/test/` or provider equivalent.
- Dev names: `<repo>-dev-<role>`.
- Test names: `<repo>-test-<role>`.
- Never copy encrypted config between stacks.

## Project Layout

```
infra/pulumi/
  Pulumi.yaml
  Pulumi.dev.yaml
  Pulumi.test.yaml
  package.json
  tsconfig.json
  index.ts
  components/
    workload.ts
    network.ts
```

## Module / Resource Skeleton

- Keep root resources in `index.ts` small.
- Put reusable infrastructure in component resources under `components/`.
- Extend `pulumi.ComponentResource` for repeated bundles.
- Accept `environment`, `namePrefix`, and provider config in component args.
- Register component outputs explicitly.
- Export snake_case stack outputs.
- Keep secrets as `pulumi.Output<string>` and mark additional outputs secret when needed.
- Avoid raw provider resource sprawl in the root program.

## Package Discipline

- Use pinned `@pulumi/pulumi`.
- Add exactly the provider packages the repo needs.
- Keep `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock` committed.
- Compile with strict TypeScript.
- Do not mix CommonJS and ESM without a deliberate local convention.

## Secrets

- Store stack secrets with `pulumi config set --secret`.
- Store provider credentials in native secret stores or CI secret systems.
- Use provider secret references for workload runtime secrets.
- Do not commit plaintext config values.
- Keep `Pulumi.dev.yaml` and `Pulumi.test.yaml` separate.

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

- Use `@pulumi/pulumi/automation` for Lane B integration harnesses.
- Select or create the test stack explicitly.
- Run preview before update when drift risk matters.
- Capture outputs for integration tests without exposing secrets.
- Destroy ephemeral test stacks by default.
- Treat preview failures as stop conditions.

## Provider Bindings

- AWS uses `@pulumi/aws`.
- GCP uses `@pulumi/gcp`.
- Azure uses `@pulumi/azure-native`.
- Kubernetes uses `@pulumi/kubernetes`.
- Keep provider instances environment-scoped when multiple accounts, projects, or subscriptions are active.

## Validation Gates

- Reference `context/doctrine/pulumi-stack-discipline.md`.
- Dev and test stacks both exist.
- Resource names include the stack name.
- Secret config values are encrypted.
- Automation tests use the `test` stack only.

## Anti-Patterns

- One Pulumi stack for every environment.
- Plain config for secret values.
- Root program containing every resource inline.
- Outputs that expose passwords or tokens.
- Automation API updates against a developer-selected current stack.
