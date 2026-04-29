# Azure Container Apps TypeScript Hono

Load this stack for Azure Container Apps services written in TypeScript with Hono. It owns the Node 20 runtime, tsup bundle, ACR image deployment, and accb container validation.

## Image Surface

- Runtime pin: Node 20 with Hono and a compiled tsup bundle.
- Registry: Azure Container Registry; tag with git SHA and deploy by digest.
- Base image: digest-pinned `node:20-slim` or distroless Node final image.
- Build: multi-stage Dockerfile with lockfile install, `npm run build`, and production dependencies only.
- User: run as non-root and avoid writable app directories.
- Security: produce an SBOM and scan with Defender for Cloud or Trivy.

## Service Surface

- Entrypoint: `node dist/server.js` listening on `${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`.
- Concurrency: model with ACA HTTP scale rules and downstream pool limits.
- Scaling: declare min replicas, max replicas, CPU, memory, ingress, and revision mode.
- Startup: keep top-level imports deterministic and bind the port before optional warmups.
- Triggers: HTTP and KEDA event sources such as Service Bus, Event Hubs, queues, and custom scalers.

## Networking

- Ingress may be external, internal, or disabled.
- Use ACA environment VNet integration when private resources are required.
- Declare private DNS, firewall rules, and public egress expectations.
- Keep event-driven private workers internal unless a public HTTP contract is required.
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

- Require idempotency headers on mutating routes.
- Derive event keys from Service Bus message id, Event Hubs metadata, or queue message id.
- Store replay state in Cosmos DB, Azure SQL, or storage tables with TTL.

## Identity Binding

- Use managed identity for ACR, Key Vault, Service Bus, storage, and database access.
- Scope RBAC to exact resources and avoid subscription-wide contributor roles.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## Secrets

- Use Key Vault references or runtime reads through managed identity.
- Keep `.env` local-only and excluded from container context.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit structured JSON logs with `service`, `env`, `revision`, `replica`, `request_id`, and `trace_id`.
- Use OpenTelemetry middleware and Azure Monitor exporters.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Using ACA as a catch-all for unbounded background loops.
- Deploying mutable image tags into test or production.
- Granting broad managed identity permissions for one queue or vault.
