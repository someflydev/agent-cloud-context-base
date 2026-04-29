# Azure Container Apps Go Echo

Load this stack for Azure Container Apps services written in Go with Echo. It owns the Go HTTP binary, ACR image deployment, ACA scaling rules, and accb container validation.

## Image Surface

- Runtime pin: Go 1.22 with Echo.
- Registry: Azure Container Registry with immutable git SHA tags.
- Base image: digest-pinned Go builder and distroless/static final image.
- Build: multi-stage Dockerfile with `CGO_ENABLED=0 go build` unless native dependencies require CGO.
- User: run as non-root in the runtime image.
- Security: generate an SBOM and scan before promotion.

## Service Surface

- Entrypoint: compiled binary listening on `${PORT:-8080}`.
- Health paths: `/healthz` and `/readyz`.
- Concurrency: tune HTTP scale target to handler CPU cost and downstream connection pools.
- Scaling: declare min replicas, max replicas, CPU, memory, ingress, and revision mode.
- Startup: keep config and telemetry initialization bounded.
- Triggers: HTTP and KEDA event sources including Service Bus, Event Hubs, queues, and custom scalers.

## Networking

- Ingress can be external, internal, or disabled.
- Use ACA VNet integration for private endpoints, Azure SQL private links, caches, or internal services.
- Declare DNS, firewall rules, and outbound public dependencies.
- Keep private workers without external ingress.
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

- Require idempotency keys for mutating HTTP endpoints.
- Derive event keys from Service Bus, Event Hubs, queue, or custom scaler payload identity.
- Store replay records in Cosmos DB, Azure SQL, or storage tables.

## Identity Binding

- Use managed identity per app or related app group.
- Scope RBAC to exact ACR, Key Vault, messaging, storage, and database resources.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## Secrets

- Use Key Vault with managed identity.
- Keep credentials out of build args, image labels, and source.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit JSON logs with `service`, `env`, `revision`, `replica`, `request_id`, `trace_id`, and `outcome`.
- Use OpenTelemetry HTTP middleware and Azure Monitor metrics.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Shipping the Go toolchain in the runtime image.
- Using external ingress for event-only workers.
- Claiming private network support without deployed reachability tests.
