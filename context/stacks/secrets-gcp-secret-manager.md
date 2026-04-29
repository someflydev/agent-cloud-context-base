# Secrets GCP Secret Manager

Load this stack for Google Cloud Secret Manager in accb-derived repos. It owns secret storage, service-account bindings, Workload Identity access, Cloud Run secret injection, rotation, and validation.

## Capability Surface

- Primary store: Google Cloud Secret Manager.
- Dev secret name: `<repo>-dev-<secret>`.
- Test secret name: `<repo>-test-<secret>`.
- Dev env-var prefix: `ACCB_DEV_GCP_`.
- Test env-var prefix: `ACCB_TEST_GCP_`.
- Dev resource names: `<repo>-dev-<role>`.
- Test resource names: `<repo>-test-<role>`.
- Use automatic replication unless residency requirements demand user-managed replication.
- Reference `context/doctrine/cloud-secret-handling.md`.

## Storage Pattern

- Store credentials, tokens, and connection strings as Secret Manager secrets.
- Use versions for rotation and rollback.
- Label secrets with project, environment, owner, and rotation owner.
- Use CMEK only when platform requirements call for it.
- Keep secret values out of Terraform variables and Pulumi plain config.
- Pass secret resource names to workloads.

## Service Account Binding

- Grant `roles/secretmanager.secretAccessor` only to consuming service accounts.
- Bind at the secret resource when possible.
- Avoid project-wide accessor grants.
- Keep deployer secret permissions separate from workload permissions.
- Use IAM Conditions when useful and supported.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## Workload Identity

- For GKE, bind Kubernetes service accounts to Google service accounts through Workload Identity.
- Keep namespace and service account subjects environment-specific.
- Avoid mounting static JSON keys into pods.
- Use External Secrets Operator when Kubernetes Secret materialization is required.
- Keep dev and test identity bindings disjoint.

## Cloud Run Pattern

- Prefer Cloud Run secret environment variables or volume mounts for simple values.
- Use runtime SDK fetch when the application needs dynamic version selection.
- Pin to a version for deterministic tests.
- Use `latest` only when rotation behavior is deliberate.
- Keep plaintext values out of deployment YAML.

## Rotation

- Create a new secret version for rotated values.
- Disable old versions after the recovery window.
- Record rotation owner and cadence in manifests.
- Exercise a smoke test after rotation.
- Alert on failed secret access after deployment.
- Keep audit logs enabled for secret reads.

## CLI Surface

```bash
gcloud secrets describe <repo>-dev-<secret>
gcloud secrets versions access latest --secret=<repo>-test-<secret>
gcloud secrets add-iam-policy-binding <secret> --member=<member> --role=roles/secretmanager.secretAccessor
```

## Validation Gates

- Dev and test secret names differ.
- Accessor bindings target workload service accounts.
- No JSON service account keys are committed.
- Workload Identity is used for GKE.
- Secret values are absent from source and IaC inputs.

## Anti-Patterns

- Project-wide secret accessor by default.
- Static service account key files.
- Shared secrets across dev and test.
- Plaintext secret values in Cloud Run env vars.
- Logging secret payloads.
