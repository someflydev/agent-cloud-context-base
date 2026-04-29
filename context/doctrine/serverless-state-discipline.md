# Serverless State Discipline

Functions are stateless by contract. Any state that matters after a retry, cold start, deployment, or scale-out must live in a managed store with a declared ownership boundary.

## Keep Handlers Stateless

- Do not depend on in-process memory across invocations.
- Treat local file storage as ephemeral and bounded.
- Do not coordinate workflow state through temporary files.
- Cache only data that can be recomputed or refetched.
- Keep idempotency outside process memory.

## Place Persistent State

- Use object storage for large blobs.
- Use document stores for workflow state, dedupe markers, and event records.
- Use relational stores for transactional records.
- Use vector stores for embeddings and retrieval indexes.
- Use managed workflow state machines for multi-step orchestration.

## Use Cache Carefully

- Use Redis, Memorystore, or Azure Cache for read-through and short-lived coordination.
- Do not use cache as the primary system of record.
- Give cached values explicit TTLs.
- Make cache loss a tested condition when it affects behavior.
- Keep cache credentials in the provider secret store.

## Prove State Behavior

- Test duplicate delivery against persisted dedupe markers.
- Test retry behavior after a simulated cold start.
- Test persistence at the managed-service boundary.
- Verify IAM or service account access to state resources through IaC.
- Stop when state ownership is unclear.
