# Canonical Terraform IaC: Azure

This starter isolates `dev` and `test` Azure surfaces for an `.accb/` generated
repo. It models Function Apps, Blob Storage, Cosmos DB, Service Bus with DLQ
semantics, Key Vault, and managed identity.

Isolation contract:

- State: `dev/backend.tf` and `test/backend.tf` use different blob keys.
- Env prefix: `environment` is propagated into every module resource name.
- Secrets: Key Vault names and secret names are environment-scoped.
- Resources: names include `accb-${var.environment}`.
