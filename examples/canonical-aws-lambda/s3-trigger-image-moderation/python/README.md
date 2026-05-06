# S3 Trigger Image Moderation (Python)

AWS Lambda handles S3 `ObjectCreated` events, validates image metadata, calls
Rekognition for labels and moderation, records exactly-once processing in
DynamoDB by object version, and emits an EventBridge event for flagged images.

Dev/test isolation:

- Terraform state: `accb/canonical-aws-lambda/s3-trigger-image-moderation/python/dev.tfstate` and `.../test.tfstate`
- Pulumi stacks: `dev` and `test`
- Env-var prefixes: `ACCB_DEV_` and `ACCB_TEST_`
- Secret paths: `/accb/dev/s3-trigger-image-moderation/*` and `/accb/test/s3-trigger-image-moderation/*`
- Resource names: `accb-${environment}-s3mod-*`

Cost band for Lane B ephemeral real AWS: low, normally under USD 1 for short
validation runs, excluding account-specific logging retention and data transfer.

## Verify

```bash
bash examples/canonical-aws-lambda/s3-trigger-image-moderation/python/tests/verify.sh
```

Lane A requires Docker and ministack:

```bash
cd examples/canonical-aws-lambda/s3-trigger-image-moderation/python/tests/integration/lane-a-ministack
./run.sh
```

Lane B requires AWS credentials and creates real resources:

```bash
cd examples/canonical-aws-lambda/s3-trigger-image-moderation/python/tests/integration/lane-b-ephemeral-real
./up.sh
timeout 1800 python3 test_handler.py
./down.sh
```
