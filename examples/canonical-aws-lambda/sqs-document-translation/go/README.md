# SQS Document Translation (Go)

SQS invokes Lambda, which fetches a source document from S3, translates it with
Amazon Translate, writes the translated artifact to destination S3, records job
status in DynamoDB, and relies on an SQS DLQ for terminal failures. The handler
uses the SQS message ID as the replay unit and checks remaining Lambda time
before starting work.

Dev/test isolation:

- Terraform state: `accb/canonical-aws-lambda/sqs-document-translation/go/dev.tfstate` and `.../test.tfstate`
- Pulumi stacks: `dev` and `test`
- Env-var prefixes: `ACCB_DEV_` and `ACCB_TEST_`
- Secret paths: `/accb/dev/sqs-document-translation/translate` and `/accb/test/sqs-document-translation/translate`
- Resource names: `accb-${environment}-translate-*`

Cost band for Lane B ephemeral real AWS: low, normally under USD 1 for short
validation runs, excluding account-specific logging retention and data transfer.

## Verify

```bash
bash examples/canonical-aws-lambda/sqs-document-translation/go/tests/verify.sh
```

Build the Lambda deployment artifact before running Terraform or Pulumi:

```bash
cd examples/canonical-aws-lambda/sqs-document-translation/go
./package.sh
```

Lane A requires Docker and ministack:

```bash
cd examples/canonical-aws-lambda/sqs-document-translation/go/tests/integration/lane-a-ministack
./run.sh
```
