# Multi Environment Promotion

Dev and test are first-class environments. Promotion means applying the same declared infrastructure and artifact choices to the next environment, not copying mutable cloud state.

## Treat Dev And Test As Real

- Create dev and test with separate state.
- Use separate secrets for dev and test.
- Use separate resource names for dev and test.
- Use separate workload identities for dev and test.
- Keep both environments visible in manifests and IaC inputs.

## Promote Through IaC

- Promote dev to test by applying Terraform or Pulumi against the test workspace or stack.
- Do not copy dev databases, queues, buckets, or secrets into test as promotion.
- Promote container images by immutable tag, not rebuild.
- Promote function packages through the packaging contract declared by the stack.
- Verify test after apply before claiming promotion complete.

## Keep Prod Operator Driven

- Recognize prod as a possible environment.
- Never create prod automatically from the base.
- Require derived repos to document their own prod promotion contract.
- Keep prod credentials and state out of generated dev/test defaults.
- Stop when a task asks for prod without naming an operator-owned policy.

## Preserve Isolation

- Use disjoint state backend keys or stacks per environment.
- Use environment-specific secret paths and KMS keys or aliases.
- Include the environment in every resource name.
- Keep teardown rules environment-specific.
- Run isolation validation after touching IaC.
