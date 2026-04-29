# Cloud Secret Handling

Secrets must live in provider-native secret systems and reach workloads through identity-based access. Copying secret values through source, IaC variables, images, or logs turns deployment plumbing into a credential leak.

## Store Secrets Natively

- Use AWS Secrets Manager or Systems Manager Parameter Store for AWS workloads.
- Use GCP Secret Manager for GCP workloads.
- Use Azure Key Vault for Azure workloads.
- Keep secret paths environment-specific.
- Avoid local files as the source of truth for deployed secrets.

## Bind Through Identity

- Grant secret access to the workload identity.
- Resolve secrets at runtime or through platform-native secret references.
- Avoid plain environment variables populated by copy/paste IaC values.
- Keep secret permissions separate from general resource permissions.
- Verify access through the same identity used in deployment.

## Keep Values Out Of Code

- Never commit secret values.
- Never place secret values in `.tfvars`.
- Never store Pulumi config values without `--secret`.
- Never bake secret values into container images.
- Never print secret values in logs, traces, metrics, or test output.

## Separate Environments

- Use disjoint dev and test secret paths.
- Use separate encryption keys or aliases when keys are managed by IaC.
- Use different names for dev and test credentials.
- Prevent test workloads from reading dev secrets.
- Prevent dev workloads from reading test secrets.

## Declare Rotation

- Treat rotation cadence as a manifest concern.
- Name each secret family and its expected rotation owner.
- Prefer provider-native rotation where available.
- Document manual rotation steps when automation is not present.
- Add validation or smoke checks that rotated secrets are consumed correctly.
