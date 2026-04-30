# Add Cloud Database Integration

Use this workflow when wiring a managed database such as DynamoDB, Firestore, Cosmos DB, RDS, Cloud SQL, or Azure SQL to a cloud workload.

## Preconditions

- Database service, data model, access pattern, and workload consumer are known.
- Dev/test database resources, state, identities, secret paths, and names are disjoint.
- SQL connection strategy or document SDK access pattern is chosen.

## Sequence

1. Author IaC for the managed database, table, collection, account, or schema owner.
2. Choose the connection pattern: direct SDK for document stores, proxy or managed connector for SQL where appropriate.
3. Add migrations for SQL and keep migration state environment-specific.
4. Bind workload identity or secret reference with least privilege.
5. Add runtime repository/client code with explicit timeouts and retry behavior.
6. Add idempotency or conditional write behavior for mutating event paths.
7. Add unit tests for query construction and data mapping.
8. Add a real-roundtrip integration test in test: write, read, update or query, and cleanup.
9. Verify IaC plan/preview and dev/test isolation.

## Outputs

- Managed database IaC, migration or schema files, identity or secret binding, runtime access code, and roundtrip tests.

## Validation Gates

- `storage-real-roundtrip-in-test-stack` from `profile-rules.json`
- `identity-least-privilege-declared`
- `secret-not-in-source`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/managed-service-selection.md`
- `context/doctrine/serverless-state-discipline.md`
- `context/stacks/storage-gcp-gcs-firestore-cloudsql.md`

## Common Pitfalls

- Treating a local in-memory database test as managed database proof.
- Sharing migration state across dev and test.
- Granting broad database admin permissions to the application workload.
