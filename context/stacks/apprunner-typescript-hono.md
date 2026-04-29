# App Runner TypeScript Hono

Load this stack for AWS App Runner services written in TypeScript with Hono. It owns the Node 20 runtime, tsup bundle, ECR or source connection deployment, and accb container validation.

## Image Surface

- Runtime pin: Node 20 with Hono and a compiled tsup bundle.
- Registry: ECR image source preferred; source-code connection acceptable with reproducible build settings.
- Base image: digest-pinned `node:20-slim` or distroless Node for the runtime stage.
- Build: multi-stage Dockerfile with `npm ci`, `npm run build`, and production dependencies only in the final image.
- User: run as non-root and keep writable paths limited to `/tmp`.
- Security: produce an SBOM and scan the ECR image before deploy.

## Service Surface

- Entrypoint: `node dist/server.js` listening on `${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`; App Runner health check targets liveness.
- Concurrency: tune App Runner concurrency against the Node event loop and downstream pool limits.
- Scaling: declare min size, max size, CPU, memory, and concurrency.
- Startup: keep top-level imports deterministic and avoid network calls before the server binds.
- Triggers: HTTP only. Use Lambda, ECS, or EventBridge for background work.

## Networking

- Default ingress is public HTTPS.
- Use application auth, WAF, or upstream controls for public APIs.
- Attach an App Runner VPC connector for private RDS, ElastiCache, or private endpoint access.
- Declare outbound internet needs because VPC egress changes routing and cost.
- Reference `context/doctrine/vpc-and-private-networking.md` and `context/stacks/apprunner-vpc-connector.md`.

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

- Require idempotency headers for mutating HTTP requests.
- Store replay state in DynamoDB or RDS with effect checksum and TTL.
- Include caller identity and route in the dedupe record to avoid cross-tenant collisions.

## Identity Binding

- Use a service-specific instance role and source access role.
- Scope policies to exact ECR repository, secrets, logs, data stores, and event destinations.
- Reference `context/stacks/identity-aws-iam.md`.

## Secrets

- Use Secrets Manager or SSM Parameter Store references through App Runner runtime configuration.
- Keep `.env` files out of image context and deployment configuration.
- Reference `context/stacks/secrets-aws-secrets-manager.md`.

## Observability

- Emit structured logs with `service`, `env`, `request_id`, `trace_id`, route, and outcome.
- Use OpenTelemetry middleware and AWS exporters where appropriate.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Treating App Runner as a worker host.
- Deploying source connections without lockfile and build command discipline.
- Marking readiness green before required private dependencies are reachable.
