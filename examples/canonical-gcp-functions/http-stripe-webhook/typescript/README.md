# HTTP Stripe Webhook

TypeScript Cloud Functions Gen2 seed for `canonical-gcp-functions`.

Flow: HTTP request -> Stripe signature verification using Secret Manager ->
Firestore raw event and dedupe store -> Cloud Tasks or Workflows fulfillment
handoff -> `202 Accepted`. Replay safety uses the Stripe event ID as the
dedupe key.

Isolation surface:

- Dev state: `accb/canonical-gcp-functions/http-stripe-webhook/dev/terraform.tfstate`
- Test state: `accb/canonical-gcp-functions/http-stripe-webhook/test/terraform.tfstate`
- Dev env prefix: `ACCB_DEV_GCP_`
- Test env prefix: `ACCB_TEST_GCP_`
- Dev secret path: `projects/accb-dev-gcp-project/secrets/accb-dev-gcp-stripe-*`
- Test secret path: `projects/accb-test-gcp-project/secrets/accb-test-gcp-stripe-*`
- Resource names: `accb-dev-gcp-stripe-*` and `accb-test-gcp-stripe-*`

Run default verification:

```bash
bash examples/canonical-gcp-functions/http-stripe-webhook/typescript/tests/verify.sh
```

Lane A uses minisky and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses
real GCP credentials against an isolated test project, may incur cost, and must
destroy resources immediately after verification.
