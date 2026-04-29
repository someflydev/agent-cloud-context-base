# Cloud Run TypeScript Hono

Load this stack for Google Cloud Run services written in TypeScript with Hono. It owns the Node runtime, tsup bundle, Artifact Registry image boundary, and accb container validation.

## Image Surface

- Runtime pin: Node 20 with Hono and a compiled tsup bundle.
- Registry: Artifact Registry; publish git SHA tags and deploy by digest.
- Base image: digest-pinned `node:20-slim` or distroless Node for the final stage.
- Build: multi-stage Dockerfile with dependency install, `npm run build`, and final runtime containing `dist/` plus production dependencies only.
- User: run with the built-in non-root node user or a fixed non-root UID.
- Security: generate an SBOM and scan the image before promotion.

## Service Surface

- Entrypoint: `node dist/server.js` listening on `${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`.
- Concurrency: tune Cloud Run request concurrency around the Node event loop and outbound pool limits.
- Scaling: declare min instances, max instances, timeout, memory, CPU, and CPU throttling behavior.
- Startup: keep module initialization small; lazy-load optional clients after readiness-critical dependencies are known.
- Triggers: HTTP public, HTTP IAM-gated, Pub/Sub push, and Eventarc receivers.

## Networking

- Default reachability is public HTTPS with Cloud Run ingress controls.
- Use IAM-gated invoker access for internal service calls.
- Add Serverless VPC Access or Direct VPC egress only for named private dependencies.
- Document outbound API allowlists, DNS, and private endpoint expectations.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
src/
  server.ts
  routes.ts
  settings.ts
  telemetry.ts
tests/
  unit/
  integration/
Dockerfile
package.json
tsconfig.json
```

## Local Run

```bash
npm run build
docker build -t <app_name>:dev .
docker run --rm -p 8080:8080 -e PORT=8080 <app_name>:dev
npm test
```

## Idempotency Pattern

- Require an idempotency header for mutating routes.
- Derive replay keys from Pub/Sub `messageId`, Eventarc CloudEvent `id` plus `source`, or HTTP idempotency headers.
- Store effect checksums in Firestore, Cloud SQL, or another declared durable store.

## Identity Binding

- Use one Cloud Run service account per service or tightly related group.
- Scope IAM roles to exact Pub/Sub topics, Secret Manager secrets, storage buckets, and database access.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## Secrets

- Use Secret Manager references or runtime SDK reads through the service account.
- Keep `.env` local-only and excluded from generated deployment artifacts.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit JSON logs with `service`, `env`, `revision`, `request_id`, `trace_id`, and route outcome.
- Use OpenTelemetry instrumentation for Hono middleware and outbound clients.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Shipping TypeScript source without a reproducible build.
- Sharing broad project editor roles with the runtime service account.
- Readiness probes that ignore required downstream dependencies.
