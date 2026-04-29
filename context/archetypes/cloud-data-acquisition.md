# Cloud Data Acquisition

Use this archetype for cloud-side acquisition systems that fetch external sources, archive raw payloads to object storage, normalize data into managed storage, and optionally publish downstream events. It usually mixes scheduled or HTTP functions with a container worker when parsing, crawling, or transformation exceeds function limits.

## Common Goals

- Store immutable raw payloads before normalization.
- Normalize records into managed database or search storage with idempotency.
- Separate source fetch, parsing, persistence, and downstream publication.
- Protect external API credentials through provider-native secret binding.
- Guard cost, quota, and retry behavior for external source access.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/managed-service-selection.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/cost-and-quota-awareness.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+function or provider+container stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-aws-lambda/`, `examples/canonical-cloudrun/`, or peer provider families

## Common Workflows

- `context/workflows/add-cloud-function.md`
- `context/workflows/add-managed-container-service.md`
- `context/workflows/add-cloud-storage-integration.md`
- `context/workflows/add-cloud-database-integration.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/func-aws-lambda-python.yaml`
- `manifests/func-gcp-cloudfn-python.yaml`
- `manifests/container-cloudrun-fastapi.yaml`
- `manifests/container-aca-jobs.yaml`

## Likely Examples

- `examples/canonical-aws-lambda/scheduled-source-archive/`
- `examples/canonical-gcp-functions/http-source-normalizer/`
- `examples/canonical-cloudrun/heavy-parser-worker/`

## Typical Anti-Patterns

- Normalizing external data without preserving the raw payload.
- Retrying partner APIs without quota and backoff guardrails.
- Letting parser failures overwrite the last known good artifact.
- Treating a container crawler as an always-on API with no run key.
- Storing API tokens in source-controlled configuration.

## Validation Gates (summary)

- storage-real-roundtrip-in-test-stack: Source ingestion writes and reads through real managed storage in test.
- function-idempotency-proof: Replaying the same source item creates exactly one persisted result.
- eventing-dlq-path: Failed source records have a bounded recovery path.
- secret-binding-via-identity: Source credentials come from provider secret binding.
