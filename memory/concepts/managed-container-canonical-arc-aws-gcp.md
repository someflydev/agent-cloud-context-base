# Managed Container Canonical Arc: AWS and GCP

PROMPT_21 added the first managed-container seed examples for `accb`.
PROMPT_28 completes the required AWS/GCP managed-container expansion surface:
five Cloud Run examples and three App Runner examples.

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

Expansion examples:

- `examples/canonical-cloud-run/public-api-private-worker-job/go-echo/`
  and `examples/canonical-cloud-run/public-api-private-worker-job/typescript-hono/`
  provide the same public API, private worker callback, and scheduled cleanup
  workflow for Go Echo and TypeScript Hono.
- `examples/canonical-cloud-run/cloudrun-job-nightly-report/python-fastapi/`
  models a standalone scheduled Cloud Run Job for nightly reporting with
  isolated state, report storage, and Secret Manager references.
- `examples/canonical-app-runner/public-api-with-vpc-connector/go-echo/`
  provides the VPC Connector workflow for Go Echo.
- `examples/canonical-app-runner/supplier-onboarding/python-fastapi/`
  models an App Runner supplier onboarding API with private database reachability,
  supplier document storage, and review queue handoff.

Managed-container examples use a shifted layout from function examples:
`Dockerfile`, `src/`, health/readiness endpoints, local-container Lane A,
and ephemeral-real Lane B.

PROMPT_29 completes the managed-container expansion arc with the remaining
Azure Container Apps examples.
