# EventBridge CDC Relay - TypeScript

EventBridge change events invoke Lambda, the handler claims the source event id, stores relay status in DynamoDB, and republishes a normalized CDC event for downstream consumers.

## Dev/Test Isolation

- Terraform state: `accb/canonical-aws-lambda/eventbridge-cdc-relay/typescript/dev.tfstate` and `.../test.tfstate`
- Environment variables: `ACCB_DEV_*` and `ACCB_TEST_*`
- Secret paths: `/accb/dev/eventbridge-cdc-relay/*` and `/accb/test/eventbridge-cdc-relay/*`
- Resource names: `accb-${environment}-eventbridge-cdc-relay-*`

## Verification

```bash
bash examples/canonical-aws-lambda/eventbridge-cdc-relay/typescript/tests/verify.sh
```

Lane A uses ministack and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses ephemeral real AWS resources, requires explicit AWS credentials, incurs real cost, and must be destroyed immediately after verification.
