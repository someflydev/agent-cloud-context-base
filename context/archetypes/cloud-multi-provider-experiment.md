# Cloud Multi Provider Experiment

Use this archetype for comparative AWS, GCP, and Azure surfaces for one workload. It is not a generic abstraction layer; it is a structured experiment that lets each provider use native triggers, managed containers, eventing, storage, secrets, and IaC while preserving a common workload contract and evidence format.

## Common Goals

- Define one workload contract and compare provider-native implementations.
- Keep AWS, GCP, and Azure stacks separately deployable and testable.
- Record provider-specific behavior instead of hiding it under a leaky wrapper.
- Use explicit dev/test isolation for every provider.
- Require each provider implementation to pass its own gates before comparing.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/managed-service-selection.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/doctrine/identity-and-least-privilege.md`
- provider-specific function or managed-container stack packs for AWS, GCP, and Azure
- provider-specific IaC stack packs for AWS, GCP, and Azure
- one canonical example from each provider family when available

## Common Workflows

- `context/workflows/add-aws-lambda-trigger.md`
- `context/workflows/add-gcp-cloud-function-trigger.md`
- `context/workflows/add-azure-function-trigger.md`
- `context/workflows/add-managed-container-service.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/multi-provider-event-pipeline.yaml`
- `manifests/func-aws-lambda-python.yaml`
- `manifests/func-gcp-cloudfn-python.yaml`
- `manifests/func-azure-fn-python.yaml`
- `manifests/container-cloudrun-fastapi.yaml`
- `manifests/container-apprunner-fastapi.yaml`
- `manifests/container-aca-dotnet.yaml`

## Likely Examples

- `examples/canonical-aws-lambda/s3-trigger-image-moderation/`
- `examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/`
- `examples/canonical-azure-functions/blob-trigger-receipt-ocr/`
- `examples/canonical-cloudrun/public-api-private-worker-job/`

## Typical Anti-Patterns

- Hiding provider-specific behavior under a leaky shared abstraction.
- Declaring victory after only one provider passes its gates.
- Sharing state, secret paths, or resource names across providers.
- Forcing one provider's event model onto the others.
- Comparing cost or latency without identical workload fixtures.

## Validation Gates (summary)

- comparative-parity-evident: Each provider implementation passes provider-specific gates.
- function-trigger-contract: Function variants use real provider trigger fixtures.
- container-health-and-readiness: Container variants pass provider readiness checks.
- iac-dev-test-disjoint: Each provider uses separate dev/test state, names, and secret paths.
