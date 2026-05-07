# GCS Trigger OCR To Firestore (Go)

Cloud Storage object create events invoke a Gen2 Cloud Function, run Vision OCR, write metadata to Firestore, and publish a downstream Pub/Sub message. Idempotency is keyed by bucket, object name, and generation.

## Dev/Test Isolation

Terraform uses disjoint GCS backend prefixes for `dev` and `test`. Pulumi uses separate `dev` and `test` stacks. Environment variables use `ACCB_DEV_GCP_` and `ACCB_TEST_GCP_`; Secret Manager names use `accb-dev-*` and `accb-test-*`; resources include the environment in their names.

## Verification

```bash
bash examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/go/tests/verify.sh
```

Lane A minisky coverage is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B deploys isolated test GCP resources, can incur real cost, and must be destroyed immediately after verification.
