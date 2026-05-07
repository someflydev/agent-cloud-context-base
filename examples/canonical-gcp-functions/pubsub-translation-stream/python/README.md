# Pub/Sub Translation Stream (Python)

Pub/Sub messages carrying source documents invoke a Gen2 Cloud Function, translate text, persist translated artifacts and job status, and publish completion events. Idempotency is keyed by Pub/Sub message ID plus target locale.

## Dev/Test Isolation

Terraform uses disjoint GCS backend prefixes for `dev` and `test`. Pulumi uses separate `dev` and `test` stacks. Environment variables use `ACCB_DEV_GCP_` and `ACCB_TEST_GCP_`; Secret Manager names use `accb-dev-*` and `accb-test-*`; resources include the environment in their names.

## Verification

```bash
bash examples/canonical-gcp-functions/pubsub-translation-stream/python/tests/verify.sh
```

Lane A minisky coverage is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B deploys isolated test GCP resources, can incur real cost, and must be destroyed immediately after verification.
