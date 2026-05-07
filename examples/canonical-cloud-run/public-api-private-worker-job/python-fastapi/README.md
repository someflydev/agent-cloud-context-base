# Cloud Run public API, private worker, and job

Python service seed for `accb` managed-container generation.

Flow: public Cloud Run service receives `/submit` -> Firestore workflow
state -> GCS attachments -> Pub/Sub review fan-out -> IAM-gated private
worker callback -> scheduled Cloud Run Job cleanup.

Dev/test isolation surface:

- State: Terraform `dev` and `test` backends use distinct prefixes; Pulumi
  stacks are `dev` and `test`.
- Env-var prefix: `ACCB_CLOUDRUN_PUBLIC_WORKER_DEV_` and
  `ACCB_CLOUDRUN_PUBLIC_WORKER_TEST_`.
- Secret path: `/accb/dev/cloudrun/public-worker/reviewer` and
  `/accb/test/cloudrun/public-worker/reviewer`.
- Resource naming: `accb-${environment}-cloudrun-public-worker-*`.

Lane A runs the container locally with a `minisky` sidecar. Lane B creates
isolated real GCP test resources and must be torn down immediately.
Expected Lane B cost band: low, bounded by one Cloud Run service revision,
one private service, one scheduled job, Firestore, GCS, Pub/Sub, and Secret
Manager test resources.

Run default verification:

```bash
bash examples/canonical-cloud-run/public-api-private-worker-job/python-fastapi/tests/verify.sh
```
