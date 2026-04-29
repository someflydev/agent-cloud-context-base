# App Runner Go Echo

Load this stack for AWS App Runner services written in Go with Echo. It owns the Go HTTP binary, ECR image deployment, request scaling, and accb container validation.

## Image Surface

- Runtime pin: Go 1.22 with Echo.
- Registry: ECR image source with immutable git SHA tags.
- Base image: digest-pinned Go builder and distroless/static final image.
- Build: multi-stage Dockerfile with `CGO_ENABLED=0 go build` unless native libraries are required.
- User: run as non-root in the final image.
- Security: generate an SBOM and scan through ECR or Trivy before promotion.

## Service Surface

- Entrypoint: compiled binary listening on `${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`; configure App Runner health check.
- Concurrency: size concurrency for handler CPU use and downstream connection limits.
- Scaling: declare min size, max size, CPU, memory, and concurrency.
- Startup: avoid long network initialization before the HTTP listener binds.
- Triggers: HTTP only. Use Lambda, ECS, or EventBridge for background and scheduled work.

## Networking

- Default ingress is public HTTPS.
- Use a VPC connector for outbound private RDS, ElastiCache, internal ALB, or private endpoint access.
- Declare security groups, subnet selection, DNS, and public egress requirements.
- Avoid VPC attachment for public AWS APIs unless a private endpoint is required.
- Reference `context/doctrine/vpc-and-private-networking.md` and `context/stacks/apprunner-vpc-connector.md`.

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

- Require idempotency keys for mutating routes.
- Store key, caller, effect checksum, status, and TTL in DynamoDB or RDS.
- Keep dedupe writes ahead of non-idempotent downstream effects.

## Identity Binding

- Use dedicated App Runner service roles.
- Grant least-privilege access to ECR, logs, secrets, data stores, and event destinations.
- Reference `context/stacks/identity-aws-iam.md`.

## Secrets

- Use Secrets Manager or SSM Parameter Store through runtime references.
- Keep credentials out of image build args, labels, and source.
- Reference `context/stacks/secrets-aws-secrets-manager.md`.

## Observability

- Emit JSON logs with `service`, `env`, `request_id`, `trace_id`, `route`, and `outcome`.
- Use OpenTelemetry HTTP middleware and CloudWatch metrics.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Shipping a large build image as the runtime image.
- Using mutable tags for promotion.
- Running background queue consumers in the web service process.
