# Identity AWS IAM

Load this stack for AWS identity in accb-derived repos. It owns IAM roles, policies, Lambda execution roles, ECS and App Runner task roles, EKS IRSA, Pod Identity Agent, permission boundaries, and SCP awareness.

## Capability Surface

- Workload identity: IAM role.
- Lambda identity: execution role.
- ECS identity: task role and task execution role.
- EKS identity: IRSA or EKS Pod Identity Agent.
- Dev role names: `<repo>-dev-<workload>-role`.
- Test role names: `<repo>-test-<workload>-role`.
- Dev env-var prefix: `ACCB_DEV_AWS_`.
- Test env-var prefix: `ACCB_TEST_AWS_`.
- Reference `context/doctrine/identity-and-least-privilege.md`.

## Role Pattern

- Create one role per workload boundary.
- Keep trust policies specific to the service principal or OIDC subject.
- Put managed policies behind a manifest choice.
- Prefer inline least-privilege policies for generated examples.
- Tag roles with project, environment, workload, and owner.
- Keep dev and test roles separate.

## Lambda Pattern

- Execution role trusts `lambda.amazonaws.com`.
- Attach CloudWatch Logs permissions for the function log group.
- Add data-plane permissions only for declared resources.
- Add KMS decrypt only for required keys.
- Add VPC ENI permissions only when VPC attachment is active.

## ECS And App Runner Pattern

- Separate task execution role from task role.
- Execution role pulls images and writes logs.
- Task role accesses application resources.
- App Runner service role and instance role stay distinct when both are used.
- Do not reuse deployment roles as runtime roles.

## EKS Pattern

- Use IRSA through the cluster OIDC provider for pod identities.
- Consider EKS Pod Identity Agent where it is the platform standard.
- Bind one Kubernetes service account subject to one IAM role unless justified.
- Scope trust policy by namespace and service account.
- Keep node roles separate from workload roles.

## Least Privilege

- Scope actions to exact ARNs.
- Use condition keys for source ARN, source account, VPC endpoint, tags, or KMS context when useful.
- Treat wildcard actions or resources as waivers.
- Use permission boundaries when the organization requires them.
- Respect service control policies as outer guardrails.

## CLI Surface

```bash
aws iam get-role --role-name <repo>-dev-<workload>-role
aws iam list-attached-role-policies --role-name <role>
aws iam simulate-principal-policy --policy-source-arn <arn> --action-names <action>
```

## Validation Gates

- Dev and test role ARNs differ.
- Trust policies name exact principals.
- Workload policies exclude unrelated resources.
- Secret and KMS permissions are scoped separately.
- Wildcards have visible waivers.

## Anti-Patterns

- One admin role for all workloads.
- Node instance roles used by pods.
- Deployment role reused at runtime.
- Broad `*:*` policies.
- Console-created policy attachments.
