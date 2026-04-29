# Pulumi Stack Discipline

Pulumi environments are stacks. Each stack owns its state, config, secrets, and resource names so dev and test cannot collide.

## Use One Stack Per Environment

- Use `dev` for development resources.
- Use `test` for integration verification resources.
- Treat `prod` as optional and operator-driven.
- Do not share Pulumi state files across stacks.
- Keep stack selection explicit in commands and scripts.

## Separate State And Config

- Use separate S3 keys, GCS objects, Azure containers, or Pulumi Cloud scopes per stack.
- Keep `Pulumi.dev.yaml` and `Pulumi.test.yaml` separate.
- Store secret values with `pulumi config set --secret`.
- Do not copy encrypted secret blobs between stacks.
- Store backend credentials in a provider secret store.

## Name By Stack

- Include the stack name as a suffix in every cloud resource name.
- Include the stack name in service accounts, queues, topics, buckets, and databases.
- Keep outputs named in snake_case.
- Make outputs sufficient for tests without exposing secrets.
- Avoid provider-generated defaults for referenced resources.

## Test Through Automation

- Use Pulumi Automation API as the Lane B integration harness.
- Run previews before applies when drift risk is meaningful.
- Destroy ephemeral test stacks by default after verification.
- Treat preview drift as a stop condition before integration tests.
- Record stack commands in the generated repo.
