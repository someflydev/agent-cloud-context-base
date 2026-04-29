# Cloud Run Multi Container Sidecar

Load this stack for Cloud Run services that use multiple containers, such as an application with an OpenTelemetry collector, Envoy proxy, or lightweight helper sidecar. It owns sidecar boundaries, shared volumes, startup order, and accb container validation.

## Image Surface

- Runtime pin: each container image must be digest-pinned.
- Registry: application images live in Artifact Registry; vendor images must be mirrored or pinned by digest.
- Base image: distroless or slim for custom containers; official sidecar images must be versioned and scanned.
- Build: build app and sidecar images separately unless the sidecar is a trusted external artifact.
- User: run each container as non-root where the image supports it.
- Security: generate SBOMs for custom images and record third-party image digests.

## Service Surface

- Entrypoint: one ingress container listens on `${PORT:-8080}`; sidecars expose only internal ports.
- Health paths: app `/healthz` and `/readyz`; sidecar health must feed readiness when it is required for traffic.
- Concurrency: tune request concurrency around the ingress container and proxy or collector buffering.
- Scaling: declare min/max instances, CPU, memory, timeout, and per-container resource needs.
- Startup: use Cloud Run container startup order for dependencies such as proxy before app.
- Triggers: HTTP, IAM-gated HTTP, Pub/Sub push, and Eventarc to the ingress container.

## Networking

- Default reachability is the ingress container through Cloud Run HTTPS.
- Sidecars communicate over localhost and shared volumes only.
- Attach VPC egress when the app or sidecar reaches a named private resource.
- Declare whether Envoy, OTel collector, or helpers need outbound internet or private endpoints.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
app/
  Dockerfile
sidecars/
  otel-collector.yaml
  envoy.yaml
deploy/
  service.yaml
tests/
```

## Local Run

```bash
docker compose up --build
curl -f http://localhost:8080/healthz
curl -f http://localhost:8080/readyz
```

## Idempotency Pattern

- Keep idempotency in the app container, not in the proxy or telemetry sidecar.
- Include proxy-generated request ids in logs but derive business replay keys from trigger identity.
- Persist dedupe state before sidecar-mediated outbound effects are acknowledged.

## Identity Binding

- Use one Cloud Run service account for the revision unless a platform feature supports finer separation.
- Grant only app and sidecar-required resources such as Secret Manager, telemetry export, Pub/Sub, and storage.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## Secrets

- Bind sidecar and app secrets separately by name.
- Avoid shared volume secrets unless lifecycle and permissions are explicit.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Prefer an OTel collector sidecar when export configuration is complex or cross-language.
- Correlate app, proxy, and collector logs with trace ids and Cloud Run revision.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Adding sidecars for simple single-process services.
- Letting a sidecar become the owner of business idempotency.
- Ignoring startup ordering and marking traffic ready before the proxy or collector is usable.
