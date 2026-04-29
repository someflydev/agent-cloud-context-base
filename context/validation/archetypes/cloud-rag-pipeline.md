---
accb_origin: canonical
accb_source_path: context/validation/archetypes/cloud-rag-pipeline.md
accb_role: validation
accb_version: 1
---

# Cloud Rag Pipeline Validation

Prove indexing and retrieval against a deterministic corpus in the selected
test lane. The proof must cross the storage, embedding, vector-store, and query
boundaries that the repo declares.

Proof commands should include one ingest, one index verification, one retrieval
query with expected content, secret binding checks for model or search access,
and IaC isolation validation.

Common failure modes are nondeterministic corpora, missing vector indexes,
provider credentials in source, shared test indexes, and retrieval that only
mocks the managed service. Reference managed service, secret, observability,
and IaC isolation doctrine.
