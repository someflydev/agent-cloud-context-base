# Managed Container Canonical Arc: AWS and GCP

PROMPT_21 adds the first managed-container seed examples for `accb`.

Seed examples:

- `examples/canonical-cloud-run/public-api-private-worker-job/python-fastapi/`
  models a public Cloud Run service, IAM-gated private worker callback, and
  scheduled Cloud Run Job cleanup with Firestore, GCS, Pub/Sub, and Secret
  Manager.
- `examples/canonical-cloud-run/multi-container-sidecar/python-fastapi/`
  models a two-container Cloud Run revision with a primary app container and
  OpenTelemetry Collector sidecar.
- `examples/canonical-app-runner/public-api-with-vpc-connector/python-fastapi/`
  models an App Runner public API reaching private Aurora Postgres through a
  VPC Connector with Secrets Manager credentials and ECR tag deployment.

Managed-container examples use a shifted layout from function examples:
`Dockerfile`, `src/`, health/readiness endpoints, local-container Lane A,
and ephemeral-real Lane B.

PROMPT_22 continues the managed-container seed arc with Azure Container Apps.
