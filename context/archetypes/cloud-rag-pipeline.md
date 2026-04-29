# Cloud Rag Pipeline

Use this archetype for systems that ingest documents, chunk and embed content, upsert vectors, and serve a retrieval API. It spans function and container tiers because ingestion triggers can stay small while extraction, embedding, index rebuild, and API serving may require custom images, vector stores, and stronger observability.

## Common Goals

- Keep document intake, extraction, chunking, embedding, and retrieval separate.
- Use durable storage for raw documents and derived chunk metadata.
- Upsert vectors idempotently with deterministic document and chunk ids.
- Bind model, embedding, and vector-store credentials through secrets.
- Instrument indexing and retrieval with cloud-native and OTel telemetry.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/managed-service-selection.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/observability-cloud-native.md`
- `context/stacks/observability-otel-cloud.md`
- the dominant provider+function or provider+container stack pack
- the dominant storage and vector-store stack packs
- the dominant IaC stack pack
- one canonical example from `examples/canonical-gke/`, `examples/canonical-cloudrun/`, or function families

## Common Workflows

- `context/workflows/add-cloud-storage-integration.md`
- `context/workflows/add-cloud-database-integration.md`
- `context/workflows/add-vector-store-integration.md`
- `context/workflows/add-managed-container-service.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/container-cloudrun-fastapi.yaml`
- `manifests/k8s-gke-multi-role-python.yaml`
- `manifests/k8s-aks-multi-role-typescript.yaml`
- `manifests/func-gcp-cloudfn-python.yaml`

## Likely Examples

- `examples/canonical-cloudrun/rag-ingest-retrieval-api/`
- `examples/canonical-gke/rag-knowledge-mesh/`
- `examples/canonical-azure-functions/blob-rag-indexer/`

## Typical Anti-Patterns

- Re-embedding every document on every deployment.
- Hiding model or vector credentials in environment defaults.
- Serving retrieval from stale vectors without freshness metadata.
- Combining upload, embedding, and query serving in one opaque handler.
- Calling retrieval validated without deterministic corpus assertions.

## Validation Gates (summary)

- rag-retrieval-sanity: One indexing and one retrieval query succeed against a deterministic corpus in test.
- secret-binding-via-identity: Embedding, model, or search credentials are read via identity and secret binding.
- storage-real-roundtrip-in-test-stack: Raw documents and chunk metadata round-trip through managed storage.
- eventing-dlq-path: Failed document processing lands in a replayable path.
