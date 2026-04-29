# IaC Dev Test Isolation

Dev and test cloud environments must be impossible to confuse through state, names, secrets, or identities. Isolation is declared before resource generation because retrofitting it after resources exist is risky and expensive.

## Separate State

- Use disjoint Terraform state backends or disjoint state keys for dev and test.
- Use separate Terraform workspaces only when the backend and key strategy remain clear.
- Use separate Pulumi stacks for dev and test.
- Keep Pulumi config secrets scoped to the stack that consumes them.
- Never share remote state files across dev and test resources.

## Separate Names

- Give every resource a deterministic environment suffix such as `<repo>-dev-<role>` and `<repo>-test-<role>`.
- Include the environment in buckets, queues, topics, functions, services, clusters, and identities.
- Avoid provider-generated default names when the resource is referenced by other systems.
- Keep managed resource identifiers disjoint across environments.
- Make naming predictable enough for teardown and audit.

## Separate Secrets

- Use different secret paths for dev and test.
- Use environment-specific KMS keys or key aliases when encryption keys are declared.
- Use different env-var prefixes for dev and test configuration.
- Keep test credentials out of dev application settings.
- Keep dev credentials out of test IaC variables and Pulumi config.

## Separate Identity

- Bind dev and test workloads to different IAM roles, service accounts, or managed identities.
- Scope each identity to the resources for its own environment.
- Avoid wildcard permissions that can span both dev and test.
- Make identity bindings part of Terraform or Pulumi.
- Treat click-ops identity changes as drift.

## Tear Down Tests

- Destroy ephemeral test resources by default after integration verification.
- Require explicit operator opt-in for persistent test resources.
- Keep teardown commands documented beside the test lane.
- Make retained test resources visibly named as test.
- Expect `validate_iac_isolation.py` to enforce these rules once PROMPT_17 lands.
