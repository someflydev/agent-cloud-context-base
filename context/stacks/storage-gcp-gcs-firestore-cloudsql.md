# Storage GCP GCS Firestore Cloud SQL

Load this stack for Google Cloud storage in accb-derived repos. It owns GCS, Firestore, Cloud SQL, lifecycle, encryption, indexes, private access, and identity binding.

## Capability Surface

- Object storage: Cloud Storage.
- Document storage: Firestore.
- Relational storage: Cloud SQL.
- Dev names: `<repo>-dev-<store>`.
- Test names: `<repo>-test-<store>`.
- Dev secret names: `<repo>-dev-storage-*`.
- Test secret names: `<repo>-test-storage-*`.
- Reference `context/doctrine/iac-dev-test-isolation.md`.

## GCS Pattern

- Use uniform bucket-level access.
- Enable Object Versioning when objects are business records or state inputs.
- Define lifecycle rules for retention and expiration.
- Use CMEK only when the platform requires it.
- Configure Pub/Sub or Eventarc notifications deliberately.
- Keep bucket IAM scoped to service accounts.
- Use prefixes for tenant or workload partitions.

## Firestore Pattern

- Choose Native mode for new application workloads.
- Choose Datastore mode only for inherited Datastore compatibility.
- Declare composite indexes in source.
- Keep security rules explicit when client access exists.
- Prefer service-account access for backend-only systems.
- Use TTL policies for ephemeral data when available.
- Model hot partitions before high-volume writes.

## Cloud SQL Pattern

- Choose Postgres or MySQL explicitly.
- Prefer private IP for backend services.
- Use Cloud SQL Auth Proxy or language connector when appropriate.
- Store credentials in Secret Manager.
- Use IAM database authentication when selected and tested.
- Run migrations through the workflow.
- Avoid public IP unless a manifest waiver justifies it.

## Identity Binding

- Grant bucket access by bucket and role.
- Grant Firestore access through narrow IAM roles or rules.
- Grant Cloud SQL client permissions to workload service accounts.
- Keep Secret Manager access separate from database client permission.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## CLI Surface

```bash
gcloud storage buckets describe gs://<bucket>
gcloud firestore indexes composite list
gcloud sql instances describe <instance>
```

## Observability

- Track GCS request errors and object event failures.
- Track Firestore read, write, latency, and rule-denial signals.
- Track Cloud SQL CPU, connections, storage, replication lag, and locks.
- Include resource, environment, tenant, and trace fields in logs.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates

- Dev and test resources differ.
- GCS bucket access is not public unless waived.
- Firestore indexes are declared.
- Cloud SQL credentials live in Secret Manager.
- Private IP or public IP choice is documented.

## Anti-Patterns

- Public buckets by default.
- Firestore queries requiring undeclared indexes.
- Static database passwords in app config.
- Shared database for dev and test.
- Storage-triggered handlers without idempotency.
