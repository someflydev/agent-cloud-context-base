# Eventarc Monitoring Router

Go Cloud Functions Gen2 seed for `canonical-gcp-functions`.

Flow: Eventarc Cloud Monitoring incident event -> Firestore service ownership
lookup -> BigQuery audit row -> Slack webhook from Secret Manager. Duplicate
alert suppression uses `incident_id:state` as the dedupe key.

Isolation surface:

- Dev state: `accb/canonical-gcp-functions/eventarc-monitoring-router/dev/terraform.tfstate`
- Test state: `accb/canonical-gcp-functions/eventarc-monitoring-router/test/terraform.tfstate`
- Dev env prefix: `ACCB_DEV_GCP_`
- Test env prefix: `ACCB_TEST_GCP_`
- Dev secret path: `projects/accb-dev-gcp-project/secrets/accb-dev-gcp-monitoring-router-*`
- Test secret path: `projects/accb-test-gcp-project/secrets/accb-test-gcp-monitoring-router-*`
- Resource names: `accb-dev-gcp-monitoring-router-*` and `accb-test-gcp-monitoring-router-*`

Run default verification:

```bash
bash examples/canonical-gcp-functions/eventarc-monitoring-router/go/tests/verify.sh
```

Lane A uses minisky and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses
real GCP credentials against an isolated test project, may incur cost, and must
destroy resources immediately after verification.
