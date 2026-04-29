# Cloud Control Plane

Use this archetype for a thin orchestration layer, implemented as a function or small managed container, that coordinates heavier compute such as Kubernetes Jobs, ECS tasks, Cloud Run Jobs, Container Apps Jobs, or Batch workloads. The control plane owns authorization, state transitions, and submission, while compute remains separately deployed and scaled.

## Common Goals

- Keep the orchestration surface small and auditable.
- Submit heavy work to a separate compute boundary.
- Store request, run, and reconciliation state durably.
- Use least-privilege identity for each control action.
- Make mutating requests idempotent by run key or operation id.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/managed-service-selection.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+function or provider+container stack pack
- the dominant heavy-compute stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-cloudrun/`, `examples/canonical-eks/`, or peer provider families

## Common Workflows

- `context/workflows/add-cloud-function.md`
- `context/workflows/add-managed-container-service.md`
- `context/workflows/add-cloud-job-or-task-submitter.md`
- `context/workflows/add-cloud-database-integration.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/func-aws-lambda-python.yaml`
- `manifests/container-cloudrun-fastapi.yaml`
- `manifests/container-aca-jobs.yaml`
- `manifests/k8s-eks-multi-role-python.yaml`

## Likely Examples

- `examples/canonical-cloudrun/control-plane-over-cloud-run-jobs/`
- `examples/canonical-eks/control-api-submits-k8s-jobs/`
- `examples/canonical-aca/control-api-container-apps-jobs/`

## Typical Anti-Patterns

- Letting the control plane execute heavy work inline.
- Giving the control plane broad admin access to every compute resource.
- Treating job submission as success without reconciliation.
- Making retries create duplicate downstream jobs.
- Mixing tenant or user policy into the worker image instead of the request contract.

## Validation Gates (summary)

- identity-least-privilege-declared: Control-plane actions use explicit least-privilege workload identity.
- function-idempotency-proof: Replay one mutating request and assert exactly-once managed-state effect.
- container-health-and-readiness: Container control-plane services respond to readiness checks.
- k8s-job-completion: Kubernetes-backed compute jobs complete in test when used.
