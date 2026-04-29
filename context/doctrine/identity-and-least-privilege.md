# Identity And Least Privilege

Every cloud workload needs an explicit identity and the smallest permission set that proves its contract. Identity is infrastructure, so it belongs in IaC and should be reviewed like code.

## Bind Explicit Identities

- Use an AWS IAM role for Lambda execution, ECS tasks, App Runner services, and IRSA-backed EKS pods.
- Use a GCP service account for Cloud Functions, Cloud Run, and Workload Identity-backed GKE pods.
- Use an Azure managed identity for Azure Functions, Container Apps, and Workload Identity-backed AKS pods.
- Assign one identity per workload role unless a manifest justifies sharing.
- Keep dev and test identities separate.

## Scope Permissions

- Grant only the actions required by the trigger contract.
- Scope resources to environment-specific names and identifiers.
- Restrict reads, writes, publishes, consumes, decrypts, and secret access separately.
- Prefer provider-managed condition keys where they reduce blast radius.
- Remove permissions when a workload no longer needs a resource.

## Treat Wildcards As Waivers

- Avoid wildcard actions.
- Avoid wildcard resources.
- Require a manifest waiver for any `*` resource scope.
- Explain why the provider API cannot be narrowed when a wildcard remains.
- Keep wildcard waivers visible for later hardening.

## Keep Identity In IaC

- Define roles, service accounts, managed identities, bindings, and policies in Terraform or Pulumi.
- Avoid console-created permissions.
- Avoid manual policy attachment during debugging.
- Detect click-ops changes as drift.
- Keep generated code aligned with generated IaC.

## Verify Access

- Test that the workload can access required resources.
- Test that the workload fails cleanly when denied optional resources.
- Include secret access in the identity proof path.
- Check logs for authorization failures after smoke and integration runs.
- Mark completion `blocked` when credentials or identity setup cannot be verified.
