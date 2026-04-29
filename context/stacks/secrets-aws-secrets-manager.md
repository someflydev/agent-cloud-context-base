# Secrets AWS Secrets Manager

Load this stack for AWS secret storage in accb-derived repos. It owns AWS Secrets Manager, Systems Manager Parameter Store, KMS usage, runtime access, rotation, and cross-account patterns.

## Capability Surface

- Primary store: AWS Secrets Manager.
- Secondary store: Systems Manager Parameter Store for non-rotated configuration.
- Dev path: `/accb/<repo>/dev/<secret>`.
- Test path: `/accb/<repo>/test/<secret>`.
- Dev env-var prefix: `ACCB_DEV_AWS_`.
- Test env-var prefix: `ACCB_TEST_AWS_`.
- Dev names: `<repo>-dev-<secret>`.
- Test names: `<repo>-test-<secret>`.
- Reference `context/doctrine/cloud-secret-handling.md`.

## Storage Pattern

- Use Secrets Manager for credentials, tokens, and connection strings.
- Use SecureString Parameter Store only when rotation is not required.
- Tag secrets with project, environment, owner, and rotation owner.
- Encrypt with environment-specific KMS keys when keys are managed.
- Keep secret values out of Terraform variables and Pulumi plain config.
- Store only names or ARNs in workload configuration.

## Runtime Binding

- Lambda may receive secret names or ARNs as environment variables.
- Lambda should fetch values at runtime through the AWS SDK.
- ECS, App Runner, and EKS workloads should use identity-based reads.
- Kubernetes workloads should use External Secrets Operator when available.
- Cache fetched values only within documented rotation tolerance.
- Avoid copying secret values through build pipelines.

## IAM Pattern

- Grant `secretsmanager:GetSecretValue` only for required secret ARNs.
- Grant `ssm:GetParameter` only for required parameter ARNs.
- Grant `kms:Decrypt` only for the key that protects those secrets.
- Use resource tags or path prefixes to narrow environment access.
- Prevent dev roles from reading test secrets.
- Prevent test roles from reading dev secrets.
- Reference `context/stacks/identity-aws-iam.md`.

## Rotation

- Prefer provider-native rotation for database credentials.
- Set a default 90 day rotation cadence unless the credential requires shorter.
- Record manual rotation steps when automation is not present.
- Test that workloads reload or refetch rotated values.
- Keep old versions available only for the recovery window.
- Alarm on failed rotation events.

## Cross-Account Access

- Prefer replication or environment-specific secrets over broad cross-account reads.
- When cross-account reads are required, use resource policies with exact principals.
- Scope KMS key policy to the consuming account role.
- Include source account and principal conditions where supported.
- Audit CloudTrail reads for shared secrets.

## CLI Surface

```bash
aws secretsmanager describe-secret --secret-id <repo>-dev-<secret>
aws secretsmanager get-secret-value --secret-id <repo>-test-<secret>
aws ssm get-parameter --name /accb/<repo>/dev/<name> --with-decryption
```

## Validation Gates

- Dev and test secret names differ.
- Secret values are absent from source and tfvars.
- Workload IAM role can read only declared secrets.
- Rotation owner and cadence are documented.
- KMS decrypt scope is environment-specific.

## Anti-Patterns

- Plain environment variables containing secret values.
- One shared secret for dev and test.
- Wildcard secret access.
- Secrets baked into container images.
- Logging fetched secret values.
