# Cloud Run Go Echo

Load this stack for Google Cloud Run services written in Go with Echo. It owns the Go HTTP service shape, static image build, Artifact Registry deployment, and accb container validation.

## Image Surface

- Runtime pin: Go 1.22 with Echo.
- Registry: Artifact Registry; publish immutable git SHA tags and deploy by digest.
- Base image: digest-pinned Go builder and distroless/static final image.
- Build: multi-stage Dockerfile with `CGO_ENABLED=0 go build` unless a native dependency requires CGO.
- User: run as non-root in the distroless image.
- Security: produce an SBOM and scan with Artifact Analysis or Trivy.

## Service Surface

- Entrypoint: compiled binary listening on `${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`.
- Concurrency: start from Cloud Run defaults; lower concurrency when handlers are CPU-bound.
- Scaling: declare min instances, max instances, timeout, memory, CPU, and startup CPU boost.
- Startup: initialize config and telemetry early; defer expensive client warmup unless readiness requires it.
- Triggers: HTTP public, HTTP IAM-gated, Pub/Sub push, and Eventarc receivers.

## Networking

- Default reachability is public HTTPS with optional ingress restrictions.
- Use IAM invoker for service-to-service calls.
- Attach VPC egress only for named private resources such as Cloud SQL private IP or Memorystore.
- Declare egress path, DNS behavior, and any outbound internet dependency.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
cmd/server/main.go
internal/http/
internal/settings/
internal/telemetry/
tests/
Dockerfile
go.mod
go.sum
```

## Local Run

```bash
go test ./...
docker build -t <app_name>:dev .
docker run --rm -p 8080:8080 -e PORT=8080 <app_name>:dev
```

## Idempotency Pattern

- Require idempotency keys on mutating HTTP endpoints.
- Derive event keys from Pub/Sub push message metadata or Eventarc CloudEvent identity.
- Store key, checksum, status, and TTL in Firestore, Cloud SQL, or another declared store.

## Identity Binding

- Use a dedicated Cloud Run service account.
- Grant resource-scoped roles only for the service's declared dependencies.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## Secrets

- Use Secret Manager and fetch through ADC-backed clients or secret projection.
- Keep secret values out of image layers and build args.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit JSON logs with `service`, `env`, `revision`, `request_id`, `trace_id`, and `outcome`.
- Use OpenTelemetry HTTP middleware and exported metrics.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Running a shell or package manager in the final image.
- Leaving the service as root because the image is small.
- Deploying by mutable tag instead of digest.
