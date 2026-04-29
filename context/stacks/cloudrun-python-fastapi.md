# Cloud Run Python FastAPI

Load this stack for Google Cloud Run services written in Python with FastAPI. It owns the ASGI service shape, Artifact Registry image boundary, Cloud Run revision settings, and accb container validation.

## Image Surface

- Runtime pin: Python 3.12 with FastAPI and uvicorn.
- Registry: Artifact Registry; tag with git SHA and promote by immutable digest.
- Base image: digest-pinned `python:3.12-slim` or a distroless Python image when dependencies allow it.
- Build: multi-stage Dockerfile with uv dependency sync in the build stage and only app files plus the virtual environment in the runtime stage.
- User: run as a non-root UID and keep writable paths limited to `/tmp`.
- Security: produce an SBOM, scan with Artifact Analysis or Trivy, and fail critical untriaged vulnerabilities.

## Service Surface

- Entrypoint: `uvicorn <package>.main:app --host 0.0.0.0 --port ${PORT:-8080}`.
- Health paths: `/healthz` for liveness and `/readyz` for dependency readiness.
- Concurrency: start with Cloud Run default concurrency only after load testing; lower it for CPU-bound handlers or shared connection pools.
- Scaling: declare min instances, max instances, CPU allocation, timeout, and memory in IaC.
- Startup: use min instances only when measured cold starts violate the user-facing contract.
- Triggers: HTTP public, HTTP IAM-gated, Pub/Sub push, and Eventarc with Cloud Run as receiver.

## Networking

- Default reachability is public HTTPS unless ingress is restricted.
- Use IAM invoker or internal ingress for private services.
- Attach Serverless VPC Access or Direct VPC egress only when a named private resource requires it.
- Declare DNS and egress behavior for Cloud SQL, Memorystore, private endpoints, and outbound APIs.
- Reference `context/doctrine/vpc-and-private-networking.md` for private reachability decisions.

## Project Layout

```
src/<app_name>/
  main.py
  routes.py
  settings.py
  telemetry.py
tests/
  unit/
  integration/
Dockerfile
pyproject.toml
uv.lock
```

## Local Run

```bash
docker build -t <app_name>:dev .
docker run --rm -p 8080:8080 -e PORT=8080 <app_name>:dev
uv run pytest
```

## Idempotency Pattern

- Require an idempotency key for mutating HTTP requests or derive one from Pub/Sub/Eventarc message identity.
- Store request key, effect checksum, status, and TTL in Firestore or Cloud SQL.
- Treat retries from Pub/Sub push and Eventarc as replay attempts, not new business events.

## Identity Binding

- Use a dedicated Cloud Run service account per service boundary.
- Grant only required roles on Artifact Registry, Secret Manager, Pub/Sub, storage, and databases.
- Reference `context/stacks/identity-gcp-iam-sa.md` for the PROMPT_12 identity stack.

## Secrets

- Use Secret Manager with service-account access and runtime secret projection or SDK reads.
- Inject secret names, not plaintext values, into environment variables.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit structured JSON logs with `service`, `env`, `revision`, `request_id`, `trace_id`, and `outcome`.
- Propagate `traceparent` and `X-Cloud-Trace-Context`.
- Export OpenTelemetry traces and metrics; reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Baking Google credentials into the image.
- Using `latest` for test or production promotion.
- Treating `/healthz` as ready when database or queue dependencies are required.
