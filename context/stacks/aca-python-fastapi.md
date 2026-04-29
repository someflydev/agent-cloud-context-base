# Azure Container Apps Python FastAPI

Load this stack for Azure Container Apps services written in Python with FastAPI. It owns the ASGI service shape, ACR image boundary, ACA ingress and scaling settings, and accb container validation.

## Image Surface

- Runtime pin: Python 3.12 with FastAPI and uvicorn.
- Registry: Azure Container Registry with git SHA tags and digest promotion.
- Base image: digest-pinned `python:3.12-slim` or distroless Python when dependencies allow it.
- Build: multi-stage Dockerfile with uv dependency sync and runtime-only final image.
- User: run as non-root and keep writable paths limited to `/tmp`.
- Security: generate an SBOM and scan with Defender for Cloud or Trivy.

## Service Surface

- Entrypoint: `uvicorn <package>.main:app --host 0.0.0.0 --port ${PORT:-8080}`.
- Health paths: `/healthz` for liveness and `/readyz` for readiness.
- Concurrency: set target concurrent requests through ACA HTTP scale rules.
- Scaling: declare min replicas, max replicas, CPU, memory, ingress, and revision mode.
- Startup: use min replicas when cold starts violate the contract.
- Triggers: HTTP and KEDA-driven event sources such as Service Bus, Event Hubs, queues, and custom scalers.

## Networking

- Default reachability depends on ingress: external, internal, or disabled.
- Use Container Apps environment VNet integration for private resources.
- Declare private DNS, egress, and managed identity access for Azure SQL, Cosmos DB, caches, and queues.
- Keep public egress explicit when outbound APIs are required.
- Reference `context/doctrine/vpc-and-private-networking.md`.

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
- Derive replay keys from Service Bus message id, Event Hubs partition and sequence, or queue message id.
- Store key, checksum, status, and TTL in Cosmos DB, Azure SQL, or storage tables.

## Identity Binding

- Use system-assigned or user-assigned managed identity per app boundary.
- Scope RBAC to exact ACR pulls, Key Vault, Service Bus, storage, databases, and monitoring resources.
- Reference `context/stacks/identity-azure-entra-mi.md` for the PROMPT_12 identity stack.

## Secrets

- Use Azure Key Vault references or SDK reads through managed identity.
- Inject secret names or vault URIs, not plaintext values.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit JSON logs with `service`, `env`, `revision`, `replica`, `request_id`, `trace_id`, and `outcome`.
- Export OpenTelemetry traces and metrics to Azure Monitor or another declared backend.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Using external ingress for a private worker.
- Pulling ACR images with shared credentials instead of managed identity where supported.
- Treating liveness as readiness for database-backed routes.
