# Cloud Event Pipeline

Use this archetype for trigger to enrich to persist to fan-out systems such as ingestion, CDC relay, OCR, moderation, or notification pipelines. The normal shape is function-first, with a managed container step allowed when enrichment requires heavier binaries or longer execution.

## Common Goals

- Make each pipeline stage explicit and independently testable.
- Persist raw or canonical records before irreversible transformation.
- Use provider-native eventing with bounded retry, DLQ, and replay.
- Keep idempotency keys consistent across trigger, storage, and fan-out.
- Prove the end-to-end path with real managed storage and event boundaries.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/managed-service-selection.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+function or provider+container stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-aws-lambda/`, `examples/canonical-gcp-functions/`, or `examples/canonical-azure-functions/`

## Common Workflows

- `context/workflows/add-cloud-function.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-replay-and-dlq-handling.md`
- `context/workflows/add-cloud-storage-integration.md`
- `context/workflows/add-cloud-database-integration.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/func-aws-lambda-python.yaml`
- `manifests/func-gcp-cloudfn-python.yaml`
- `manifests/func-azure-fn-python.yaml`
- `manifests/multi-provider-event-pipeline.yaml`

## Likely Examples

- `examples/canonical-aws-lambda/s3-trigger-image-moderation/`
- `examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/`
- `examples/canonical-azure-functions/blob-trigger-receipt-ocr/`

## Typical Anti-Patterns

- Dropping raw payloads after enrichment fails.
- Letting fan-out publish before the durable state write is complete.
- Treating DLQ messages as terminal instead of replayable.
- Using timestamps instead of source ids for idempotency.
- Mocking storage or eventing when validating the pipeline boundary.

## Validation Gates (summary)

- function-trigger-contract: Each pipeline stage is exercised with a real trigger.
- eventing-dlq-path: DLQ and replay path are verified.
- function-idempotency-proof: End-to-end replay assertion proves exactly-once effects.
- storage-real-roundtrip-in-test-stack: Managed storage write and read succeed in test.
