# Canonical Terraform IaC: GCP

This starter isolates `dev` and `test` GCP surfaces for an `.accb/` generated
repo. It models Cloud Functions v2, GCS, Firestore, Pub/Sub with a dead-letter
topic, Secret Manager, and a least-privilege service account.

Isolation contract:

- State: `dev/backend.tf` and `test/backend.tf` use different GCS prefixes.
- Env prefix: `environment` is propagated into every module resource name.
- Secrets: secret IDs use environment-scoped names.
- Resources: names include `accb-${var.environment}`.
