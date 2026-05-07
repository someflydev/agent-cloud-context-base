# SQS Document Translation - Python

SQS invokes Lambda, the handler claims the message id, fetches the source document from S3, translates it with Amazon Translate, writes the destination object to S3, records DynamoDB job status, and relies on the configured DLQ for terminal failures.

## Dev/Test Isolation

- Terraform state: `accb/canonical-aws-lambda/sqs-document-translation/python/dev.tfstate` and `.../test.tfstate`
- Environment variables: `ACCB_DEV_*` and `ACCB_TEST_*`
- Secret paths: `/accb/dev/sqs-document-translation/*` and `/accb/test/sqs-document-translation/*`
- Resource names: `accb-${environment}-sqs-document-translation-*`

## Verification

```bash
bash examples/canonical-aws-lambda/sqs-document-translation/python/tests/verify.sh
```

Lane A uses ministack and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses ephemeral real AWS resources, requires explicit AWS credentials, incurs real cost, and must be destroyed immediately after verification.
