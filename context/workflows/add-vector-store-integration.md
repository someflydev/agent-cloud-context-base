# Add Vector Store Integration

Use this workflow when adding provider-native or managed vector storage for cloud RAG ingestion and retrieval workloads.

## Preconditions

- Vector store choice, embedding model boundary, corpus shape, and query path are known.
- Identity or secret binding is declared for the vector store and embedding provider.
- Dev/test indexes, secret paths, state, and identities are disjoint.

## Sequence

1. Choose provider-native or managed vector storage based on required scale, filtering, latency, and provider fit.
2. Author IaC for index, collection, search service, or required network/private endpoint resources.
3. Bind workload identity or secret references with least privilege.
4. Add ingestion code for chunking, embedding, metadata, and upsert behavior.
5. Add query code for embedding, retrieval, filtering, and result shaping.
6. Declare idempotency for document re-ingestion and delete/update semantics.
7. Add unit tests for chunking, metadata, and query result shaping.
8. Add a roundtrip integration test against test: index a deterministic document, query it, assert expected retrieval, and cleanup.
9. Document teardown for indexes and any paid backing resources.

## Outputs

- Vector store IaC, identity or secret binding, ingestion path, query path, and retrieval integration test.

## Validation Gates

- `rag-retrieval-sanity` from `profile-rules.json`
- `secret-binding-via-identity`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/managed-service-selection.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/stacks/storage-gcp-gcs-firestore-cloudsql.md`

## Common Pitfalls

- Treating embedding generation as deterministic without pinning model and input.
- Sharing a dev index with test because vector stores are expensive.
- Skipping delete or update behavior in ingestion tests.
