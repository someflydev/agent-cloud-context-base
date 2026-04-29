# Azure Container Apps Dotnet ASP.NET

Load this stack for Azure Container Apps services written in .NET 8 with ASP.NET Core minimal APIs. It owns the ASP.NET container shape, chiseled Ubuntu image guidance, ACR deployment, and accb container validation.

## Image Surface

- Runtime pin: .NET 8 with ASP.NET Core minimal APIs.
- Registry: Azure Container Registry with immutable git SHA tags and digest deployment.
- Base image: digest-pinned .NET 8 chiseled Ubuntu runtime where app dependencies support it.
- Build: multi-stage Dockerfile with SDK builder and runtime-only final image.
- User: run as non-root and keep writable paths explicit.
- Security: generate an SBOM and scan with Defender for Cloud or Trivy.

## Service Surface

- Entrypoint: `dotnet <App>.dll` listening on `${PORT:-8080}` through `ASPNETCORE_URLS`.
- Health paths: `/healthz` and `/readyz` using ASP.NET health checks.
- Concurrency: tune ACA HTTP scale rules and .NET thread pool behavior through measured tests.
- Scaling: declare min replicas, max replicas, CPU, memory, ingress, and revision mode.
- Startup: keep dependency warmup bounded and visible in readiness.
- Triggers: HTTP and KEDA event sources such as Service Bus, Event Hubs, queues, and custom scalers.

## Networking

- Ingress may be external, internal, or disabled.
- Use ACA VNet integration for private Azure SQL, Cosmos DB, cache, or internal APIs.
- Declare DNS, firewall, private endpoint, and outbound public API requirements.
- Keep public egress deliberate and documented.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
src/App/
  Program.cs
  Settings/
  Telemetry/
tests/App.Tests/
Dockerfile
Directory.Packages.props
```

## Local Run

```bash
dotnet test
docker build -t <app_name>:dev .
docker run --rm -p 8080:8080 -e PORT=8080 <app_name>:dev
```

## Idempotency Pattern

- Require idempotency keys for mutating HTTP endpoints.
- Derive event replay keys from Azure messaging metadata for KEDA-triggered apps.
- Store key, checksum, status, and TTL in Cosmos DB, Azure SQL, or storage tables.

## Identity Binding

- Use managed identity for ACR pull, Key Vault, messaging, storage, and database access.
- Scope Azure RBAC assignments to exact resources.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## Secrets

- Use Key Vault configuration providers or Azure SDK reads through managed identity.
- Keep secret values out of appsettings files and container layers.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit structured logs with `service`, `env`, `revision`, `replica`, `trace_id`, and route outcome.
- Use OpenTelemetry for ASP.NET Core and Azure Monitor export.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Using legacy full framework assumptions in a container app.
- Storing Key Vault secrets in appsettings.
- Marking readiness green before required managed dependencies are reachable.
