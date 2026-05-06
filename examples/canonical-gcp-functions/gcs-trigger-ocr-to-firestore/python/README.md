# GCS Trigger OCR To Firestore

Python Cloud Functions Gen2 seed for `canonical-gcp-functions`.

Flow: Cloud Storage object create CloudEvent -> Vision OCR -> Firestore
metadata document -> Pub/Sub downstream topic. Idempotency uses
`bucket:name:generation`, so an object generation creates one OCR effect.

Isolation surface:

- Dev state: `accb/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/dev/terraform.tfstate`
- Test state: `accb/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/test/terraform.tfstate`
- Dev env prefix: `ACCB_DEV_GCP_`
- Test env prefix: `ACCB_TEST_GCP_`
- Dev secret path: `projects/accb-dev-gcp-project/secrets/accb-dev-gcp-ocr-*`
- Test secret path: `projects/accb-test-gcp-project/secrets/accb-test-gcp-ocr-*`
- Resource names: `accb-dev-gcp-ocr-*` and `accb-test-gcp-ocr-*`

Run default verification:

```bash
bash examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/python/tests/verify.sh
```

Lane A uses minisky and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses
real GCP credentials against an isolated test project, may incur cost, and must
destroy resources immediately after verification.
