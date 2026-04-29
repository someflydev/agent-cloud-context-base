# App Runner Python FastAPI

Load this stack for AWS App Runner services written in Python with FastAPI. It owns the ASGI service shape, ECR or source connection deployment, request-driven scaling, and accb container validation.

## Image Surface

- Runtime pin: Python 3.12 with FastAPI and uvicorn.
- Registry: ECR image source preferred; source-code connection acceptable for simple services with explicit build commands.
- Base image: digest-pinned `python:3.12-slim` or distroless Python where dependencies support it.
- Build: multi-stage Dockerfile with uv dependency install and runtime-only final stage.
- User: run as a fixed non-root UID and avoid writable application directories.
- Security: publish an SBOM and scan in ECR before promotion.

## Service Surface

- Entrypoint: `uvicorn <package>.main:app --host 0.0.0.0 --port ${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`; configure App Runner health checks against the liveness path.
- Concurrency: App Runner is request-driven; model scale around active requests and instance size.
- Scaling: declare min size, max size, concurrency, CPU, memory, and request timeout.
- Startup: keep import-time work small; use provisioned minimum capacity only when latency requires it.
- Triggers: HTTP only. Background work belongs in Lambda, ECS, or EventBridge-driven jobs.

## Networking

- Default ingress is public HTTPS through App Runner.
- Use private services or authentication at the application edge when public reachability is not acceptable.
- Use a VPC connector only for outbound access to private databases, caches, or endpoints.
- Declare egress rules, subnet selection, security groups, and NAT cost when internet egress is still needed.
- Reference `context/doctrine/vpc-and-private-networking.md` and `context/stacks/apprunner-vpc-connector.md`.

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

- Require idempotency keys for mutating HTTP routes.
- Store request key, caller identity, effect checksum, status, and TTL in DynamoDB or RDS.
- Treat client retries and App Runner request retries as replay attempts.

## Identity Binding

- Use a dedicated App Runner instance role and access role.
- Scope ECR, Secrets Manager, CloudWatch Logs, DynamoDB, RDS, SQS, or SNS permissions to exact resources.
- Reference `context/stacks/identity-aws-iam.md` for the PROMPT_12 identity stack.

## Secrets

- Use AWS Secrets Manager or SSM Parameter Store references, not plaintext environment values.
- Cache secrets only within documented rotation tolerance.
- Reference `context/stacks/secrets-aws-secrets-manager.md`.

## Observability

- Emit JSON logs with `service`, `env`, `request_id`, `trace_id`, `route`, and `outcome`.
- Propagate W3C trace context and AWS trace headers when present.
- Export OpenTelemetry traces and metrics; reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Running queues, schedulers, or endless background loops inside App Runner.
- Granting broad ECR or Secrets Manager access to the service role.
- Adding a VPC connector without a named private dependency.
