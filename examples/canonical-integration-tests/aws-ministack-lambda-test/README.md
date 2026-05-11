# AWS Ministack Lambda Test

Lane: local provider (Lane A). Approximate runtime: 2-5 minutes. Approximate
cost: none when run against ministack.

## Prerequisites

- `ACCB_RUN_LOCAL_PROVIDER=1`
- Docker with the ministack bundle available
- `aws` CLI configured to use the ministack endpoint URL
- Python 3 with `pytest`

When `ACCB_RUN_LOCAL_PROVIDER=1` is absent, `run.sh` exits 0 and reports the
lane as skipped. Derived repos should replace the fixture payloads with their
own event samples and keep setup/teardown idempotent.

## Flow

1. Start or connect to ministack.
2. `bootstrap.sh` creates S3, DynamoDB, and SQS resources with `test` suffixes.
3. Pytest asserts the S3 bucket, DynamoDB table, and SQS queue exist through the ministack endpoint.
4. `teardown.sh` deletes the resources.
