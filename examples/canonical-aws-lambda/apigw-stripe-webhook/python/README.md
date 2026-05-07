# API Gateway Stripe Webhook - Python

API Gateway HTTP API invokes Lambda, verifies the Stripe signature from Secrets Manager material, stores the raw event in DynamoDB with an event-id dedupe key, starts a Step Functions fulfillment workflow, and returns 202 Accepted.

## Dev/Test Isolation

- Terraform state: `accb/canonical-aws-lambda/apigw-stripe-webhook/python/dev.tfstate` and `.../test.tfstate`
- Environment variables: `ACCB_DEV_*` and `ACCB_TEST_*`
- Secret paths: `/accb/dev/apigw-stripe-webhook/*` and `/accb/test/apigw-stripe-webhook/*`
- Resource names: `accb-${environment}-apigw-stripe-webhook-*`

## Verification

```bash
bash examples/canonical-aws-lambda/apigw-stripe-webhook/python/tests/verify.sh
```

Lane A uses ministack and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses ephemeral real AWS resources, requires explicit AWS credentials, incurs real cost, and must be destroyed immediately after verification.
