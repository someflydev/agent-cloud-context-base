# S3 Trigger Image Moderation - TypeScript

S3 PutObject invokes Lambda, claims the object version, calls Rekognition label and moderation checks, records the decision in DynamoDB, and emits flagged decisions to EventBridge.

## Dev/Test Isolation

- Terraform state: `accb/canonical-aws-lambda/s3-trigger-image-moderation/typescript/dev.tfstate` and `.../test.tfstate`
- Environment variables: `ACCB_DEV_*` and `ACCB_TEST_*`
- Secret paths: `/accb/dev/s3-trigger-image-moderation/*` and `/accb/test/s3-trigger-image-moderation/*`
- Resource names: `accb-${environment}-s3-trigger-image-moderation-*`

## Verification

```bash
bash examples/canonical-aws-lambda/s3-trigger-image-moderation/typescript/tests/verify.sh
```

Lane A uses ministack and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses ephemeral real AWS resources, requires explicit AWS credentials, incurs real cost, and must be destroyed immediately after verification.
