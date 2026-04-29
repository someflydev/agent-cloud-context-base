# Identity GCP IAM Service Accounts

Load this stack for Google Cloud identity in accb-derived repos. It owns service accounts, IAM bindings, Workload Identity for GKE, Workload Identity Federation, and least-privilege role assignment.

## Capability Surface

- Workload identity: service account.
- GKE identity: Workload Identity binding.
- Cross-cloud identity: Workload Identity Federation.
- Dev service accounts: `<repo>-dev-<workload>@<project>.iam.gserviceaccount.com`.
- Test service accounts: `<repo>-test-<workload>@<project>.iam.gserviceaccount.com`.
- Dev env-var prefix: `ACCB_DEV_GCP_`.
- Test env-var prefix: `ACCB_TEST_GCP_`.
- Reference `context/doctrine/identity-and-least-privilege.md`.

## Service Account Pattern

- Create one service account per workload boundary.
- Keep display names environment-specific.
- Disable key creation unless a manifest waiver exists.
- Tag or label surrounding resources with workload and environment.
- Keep deployer identity separate from runtime identity.
- Keep dev and test service accounts separate.

## IAM Binding Pattern

- Prefer resource-level IAM bindings.
- Use project-level bindings only when the API requires them.
- Avoid primitive Owner, Editor, and Viewer roles.
- Use predefined narrow roles before custom roles.
- Use custom roles when predefined roles are materially too broad.
- Use IAM Conditions where supported.

## GKE Workload Identity

- Bind Kubernetes service accounts to Google service accounts.
- Scope member strings by namespace and Kubernetes service account.
- Keep namespace names environment-specific.
- Avoid JSON key mounts.
- Validate pod access through the same service account used in deployment.

## Workload Identity Federation

- Use federation for GitHub, CI, or cross-cloud deployment identities.
- Avoid long-lived service account keys.
- Scope pools and providers to the calling system.
- Use attribute conditions to restrict repository, branch, or external subject.
- Keep deploy and runtime federation boundaries separate.

## Least Privilege

- Grant only required actions for topics, buckets, secrets, databases, and logs.
- Keep secret access separate from data-plane access.
- Remove unused roles when workload capability changes.
- Treat broad project roles as waivers.
- Review inherited folder and organization bindings.

## CLI Surface

```bash
gcloud iam service-accounts describe <service-account-email>
gcloud projects get-iam-policy <project>
gcloud iam service-accounts get-iam-policy <service-account-email>
```

## Validation Gates

- Dev and test service accounts differ.
- No committed service account keys exist.
- Workload Identity is used for GKE workloads.
- Primitive roles are absent unless waived.
- Bindings target the narrowest practical scope.

## Anti-Patterns

- Editor role for workloads.
- Shared service account for every service.
- JSON key files in source or images.
- Project-wide secret accessor by default.
- Manual console IAM edits.
