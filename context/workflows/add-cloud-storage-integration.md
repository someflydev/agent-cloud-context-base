# Add Cloud Storage Integration

Use this workflow when wiring object storage such as S3, GCS, or Azure Blob to a cloud workload.

## Preconditions

- Provider storage service, bucket/container purpose, and workload consumer are known.
- Dev/test bucket or container names, state, secret paths, and identities are disjoint.
- Encryption, lifecycle, retention, and event notification needs are declared.

## Sequence

1. Author IaC for the bucket or container with deterministic environment naming.
2. Enable encryption, lifecycle, versioning, retention, and public access settings according to the data class.
3. Add event notifications when object changes are a trigger boundary.
4. Bind workload identity to only the needed object actions and paths.
5. Add application code for write, read, list, or signed URL behavior as required.
6. Include object version or generation in idempotency keys when overwrite behavior matters.
7. Add unit tests around object key construction and metadata handling.
8. Add a real-roundtrip integration test in test: write an object, read it back, and clean it up.
9. Run IaC plan/preview and isolation validation before completion.

## Outputs

- Object storage IaC, identity binding, runtime integration code, and real storage roundtrip test.

## Validation Gates

- `storage-real-roundtrip-in-test-stack` from `profile-rules.json`
- `identity-least-privilege-declared`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/managed-service-selection.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/stacks/storage-aws-s3-dynamodb-rds.md`

## Common Pitfalls

- Using one bucket for dev and test with prefix-only separation.
- Calling mocked object storage an integration test.
- Forgetting lifecycle rules for generated or temporary objects.
