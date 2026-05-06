# API Gateway Stripe Webhook (TypeScript)

API Gateway HTTP API invokes Lambda, which verifies the Stripe signature using
an AWS Secrets Manager secret reference, stores the raw event in DynamoDB by
Stripe event ID, starts a Step Functions fulfillment workflow once, and returns
`202 Accepted`.

Dev/test isolation:

- Terraform state: `accb/canonical-aws-lambda/apigw-stripe-webhook/typescript/dev.tfstate` and `.../test.tfstate`
- Pulumi stacks: `dev` and `test`
- Env-var prefixes: `ACCB_DEV_` and `ACCB_TEST_`
- Secret paths: `/accb/dev/apigw-stripe-webhook/signing` and `/accb/test/apigw-stripe-webhook/signing`
- Resource names: `accb-${environment}-stripe-*`

Cost band for Lane B ephemeral real AWS: low, normally under USD 1 for short
validation runs, excluding account-specific logging retention and data transfer.

## Verify

```bash
bash examples/canonical-aws-lambda/apigw-stripe-webhook/typescript/tests/verify.sh
```

Lane A requires Docker and ministack:

```bash
cd examples/canonical-aws-lambda/apigw-stripe-webhook/typescript/tests/integration/lane-a-ministack
./run.sh
```
