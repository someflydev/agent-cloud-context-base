# IaC Pulumi Python

Load this stack for Pulumi programs written in Python. It owns project layout, ComponentResource subclasses, provider package use, stack isolation, Automation API usage, and the Python CLI surface.

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
  __main__.py
  requirements.txt
  components/
    __init__.py
    workload.py
    network.py
```

## Module / Resource Skeleton

- Keep `__main__.py` as orchestration.
- Put reusable bundles in `components/`.
- Subclass `pulumi.ComponentResource`.
- Define typed args objects with dataclasses when component input grows.
- Accept `environment`, `name_prefix`, and provider handles in components.
- Call `register_outputs`.
- Export snake_case stack outputs.
- Use `Output.secret` when derived values must remain secret.
- Keep provider-specific helpers isolated by provider.

## Package Discipline

- Pin `pulumi`.
- Use `pulumi-aws`, `pulumi-gcp`, or `pulumi-azure-native` as needed.
- Keep Python runtime aligned with the generated repo.
- Prefer `uv` when the repo uses it.
- Commit the lockfile when dependency tooling creates one.

## Secrets

- Store stack secrets with `pulumi config set --secret`.
- Do not place plaintext secrets in `Pulumi.<stack>.yaml`.
- Store runtime secrets in provider-native secret stores.
- Pass secret names, IDs, or ARNs to workloads.
- Keep dev and test secret names disjoint.

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

- Use `pulumi.automation` for integration harnesses.
- Create or select `test` explicitly.
- Install dependencies before stack operations.
- Run preview before update when drift risk matters.
- Return non-secret outputs to tests.
- Destroy ephemeral test stacks by default.

## Provider Bindings

- AWS uses `pulumi_aws`.
- GCP uses `pulumi_gcp`.
- Azure uses `pulumi_azure_native`.
- Kubernetes uses `pulumi_kubernetes`.
- Use explicit provider instances when multiple targets are active.

## Validation Gates

- Reference `context/doctrine/pulumi-stack-discipline.md`.
- Dev and test stack names are explicit in scripts.
- Resource names include the stack.
- Secret config values are encrypted.
- Automation uses the test stack.

## Anti-Patterns

- Large unstructured `__main__.py` programs.
- Plaintext config secrets.
- Component resources without registered outputs.
- Resource names without environment suffixes.
- Automation that relies on the current selected stack.
