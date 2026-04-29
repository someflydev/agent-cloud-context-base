# Storage AWS S3 DynamoDB RDS

Load this stack for AWS storage in accb-derived repos. It owns S3, DynamoDB, RDS and Aurora, encryption, lifecycle, events, streams, and connection patterns.

## Capability Surface

- Object storage: S3.
- Key-value and document storage: DynamoDB.
- Relational storage: RDS or Aurora.
- Dev names: `<repo>-dev-<store>`.
- Test names: `<repo>-test-<store>`.
- Dev secret path: `/accb/<repo>/dev/storage/`.
- Test secret path: `/accb/<repo>/test/storage/`.
- Reference `context/doctrine/iac-dev-test-isolation.md`.

## S3 Pattern

- Enable block public access by default.
- Enable server-side encryption.
- Enable versioning when objects are business records or state inputs.
- Define lifecycle transitions and expiration.
- Configure event notifications to SQS, SNS, EventBridge, or Lambda deliberately.
- Scope bucket policies to exact principals.
- Use object prefixes for tenant or workload partitions.

## DynamoDB Pattern

- Use on-demand capacity unless steady throughput justifies provisioned mode.
- Declare partition keys from access patterns.
- Add sort keys only when query shape requires them.
- Define GSIs from named queries.
- Enable TTL for idempotency, dedupe, and ephemeral records.
- Use streams only when downstream processing is declared.
- Encrypt with AWS-owned or customer-managed keys as required.

## RDS Pattern

- Choose Aurora when clustering, read scaling, or fast failover matters.
- Choose standard RDS for simpler Postgres or MySQL needs.
- Prefer private subnets.
- Use RDS Proxy for Lambda or bursty connection patterns.
- Store credentials in Secrets Manager.
- Use migrations in application workflow, not ad hoc console changes.

## Identity Binding

- Grant S3 access by bucket and prefix.
- Grant DynamoDB access by table and action.
- Grant RDS access through network, IAM auth where selected, and secret access.
- Keep KMS decrypt separate.
- Reference `context/stacks/identity-aws-iam.md`.

## CLI Surface

```bash
aws s3api get-bucket-encryption --bucket <bucket>
aws dynamodb describe-table --table-name <table>
aws rds describe-db-instances --db-instance-identifier <id>
```

## Observability

- Track S3 4xx and 5xx errors when request metrics are enabled.
- Track DynamoDB throttles, consumed capacity, and stream iterator age.
- Track RDS CPU, connections, storage, replica lag, and deadlocks.
- Include resource name, environment, tenant, and request ID in logs.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates

- Dev and test storage resources differ.
- Encryption is enabled.
- Public S3 access is blocked unless explicitly waived.
- DynamoDB keys match access patterns.
- RDS credentials live in Secrets Manager.

## Anti-Patterns

- Public buckets by default.
- DynamoDB scans as the primary access path.
- Lambda directly opening unbounded database connections.
- Shared database for dev and test.
- Storage events without idempotent consumers.
