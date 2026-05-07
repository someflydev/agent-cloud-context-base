# Cloud Run multi-container sidecar

Python service seed for a two-container Cloud Run revision: primary
application container plus OpenTelemetry Collector sidecar exporting to
Cloud Trace and Cloud Logging.

Dev/test isolation surface:

- State: Terraform `dev` and `test` backends use distinct prefixes; Pulumi
  stacks are `dev` and `test`.
- Env-var prefix: `ACCB_CLOUDRUN_SIDECAR_DEV_` and
  `ACCB_CLOUDRUN_SIDECAR_TEST_`.
- Secret path: `/accb/dev/cloudrun/sidecar/otel` and
  `/accb/test/cloudrun/sidecar/otel`.
- Resource naming: `accb-${environment}-cloudrun-sidecar-*`.

Lane A runs the application container locally and may attach `minisky` for
GCP service emulation. Lane B creates isolated Cloud Run test resources and
must be destroyed immediately. Expected Lane B cost band: low, bounded by one
Cloud Run service revision plus logging and trace ingestion.
