# Secret Binding Strategy

Use this skill to choose how a workload receives secrets without leaking provider credentials, sharing environments, or bypassing cloud identity. It resolves ambiguity by classifying the secret family, selecting the provider-native store, binding through workload identity, and documenting rotation.

## Procedure

1. Identify the secret family: third-party API key, internal certificate, database credential, webhook signing secret, KMS-wrapped blob, or provider token.
2. Choose the provider-native secret store: AWS Secrets Manager, GCP Secret Manager, or Azure Key Vault.
3. Bind access through workload identity: IAM role, service account, or managed identity.
4. Avoid long-lived cloud provider credentials inside application config.
5. Declare separate dev and test secret paths before resource generation.
6. Declare env-var prefixes for references, not raw secret values.
7. Scope permissions to the exact secret versions or paths needed by the workload.
8. Set a rotation cadence in the manifest, with owner and expected compatibility behavior.
9. Add validation that proves the workload can resolve the secret in test without printing it.
10. Stop if the requested binding would mix dev and test secrets or require plaintext committed values.

## Good Triggers

- "bind a secret"
- "use Secrets Manager"
- "Key Vault binding"
- "third-party API key"
- "webhook signing secret"
- "rotation cadence"

## Avoid

- storing raw secret values in manifests, examples, or test fixtures
- sharing secret paths between dev and test
- granting broad secret access across environments
- binding secrets through user credentials instead of workload identity
- documenting a secret without a rotation expectation
