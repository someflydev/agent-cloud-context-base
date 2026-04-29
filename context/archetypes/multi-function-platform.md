# Multi Function Platform

Use this archetype for several functions that share IaC, identity, observability, and a common eventing boundary while remaining independently deployable. It fits platforms made of storage triggers, HTTP webhooks, queue workers, schedulers, or stream relays where each function owns a bounded role.

## Common Goals

- Keep each function deployable and testable as its own unit.
- Share only intentional platform code such as event envelopes and clients.
- Declare one eventing seam with retry, DLQ, and replay behavior.
- Apply least-privilege identity per function.
- Maintain dev/test isolation across every function-owned resource.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+function+language stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-aws-lambda/`, `examples/canonical-gcp-functions/`, or `examples/canonical-azure-functions/`

## Common Workflows

- `context/workflows/add-cloud-function.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-replay-and-dlq-handling.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-cloud-smoke-tests.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/func-aws-lambda-python.yaml`
- `manifests/func-gcp-cloudfn-typescript.yaml`
- `manifests/func-azure-fn-dotnet-isolated.yaml`
- `manifests/multi-provider-event-pipeline.yaml`

## Likely Examples

- `examples/canonical-aws-lambda/queue-backed-document-classifier/`
- `examples/canonical-gcp-functions/pubsub-change-relay/`
- `examples/canonical-azure-functions/servicebus-workflow-handlers/`

## Typical Anti-Patterns

- Pretending the platform is one large function with many hidden modes.
- Sharing handler code so tightly that one function cannot deploy alone.
- Omitting DLQ alarms because the functions are small.
- Giving every function the same broad service account.
- Letting replay bypass normal idempotency and audit writes.

## Validation Gates (summary)

- function-trigger-contract: Exercise each function with a real trigger event fixture.
- function-idempotency-proof: Replay each trigger and assert exactly-once effect.
- eventing-dlq-path: Verify DLQ destination, alarm, and replay path.
- identity-least-privilege-declared: Show each function has scoped identity bindings.
