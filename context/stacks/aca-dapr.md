# Azure Container Apps Dapr

Load this stack when Azure Container Apps workloads use Dapr building blocks. It owns sidecar activation, component boundaries, pub/sub and state contracts, and accb container validation.

## Image Surface

- Runtime pin: the application image remains language-specific and deployed by digest.
- Registry: application images live in ACR; Dapr sidecar version must be declared by the ACA platform settings.
- Base image: keep app images digest-pinned, slim, distroless, or chiseled as appropriate.
- Build: do not bake Dapr component secrets or config into the image.
- User: run the app container as non-root where supported.
- Security: scan the application image and review Dapr component configuration separately.

## Service Surface

- Entrypoint: the app listens on `${PORT:-8080}` and Dapr injects a sidecar for configured apps.
- Health paths: app `/healthz` and `/readyz`; include Dapr dependency readiness when Dapr is required for traffic.
- Concurrency: account for sidecar hop latency and pub/sub handler concurrency.
- Scaling: combine ACA replica settings with KEDA rules and Dapr component throughput limits.
- Startup: app readiness must wait for required Dapr components when routes depend on them.
- Triggers: HTTP plus Dapr pub/sub, state, secrets, bindings, and service invocation.

## Networking

- Dapr sidecar communicates with the app locally and external components through the ACA environment.
- Use VNet integration for private component backends such as Redis, Service Bus, or databases.
- Declare component scopes so only intended apps can use each building block.
- Keep external ingress separate from Dapr service invocation decisions.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
src/<app_name>/
  server.*
  settings.*
  telemetry.*
dapr/
  components/
  config.yaml
tests/
Dockerfile
```

## Local Run

```bash
dapr run --app-id <app_name> --app-port 8080 -- docker run --rm -p 8080:8080 <app_name>:dev
docker run --rm -p 8080:8080 <app_name>:dev
```

## Idempotency Pattern

- Derive replay keys from Dapr pub/sub message id, CloudEvent id plus source, or explicit HTTP idempotency header.
- Keep dedupe state in a durable store, not only in the Dapr sidecar.
- Ensure pub/sub handlers are safe under at-least-once delivery.

## Identity Binding

- Use managed identity for Key Vault, Service Bus, storage, and component backends where supported.
- Scope Dapr components to only the apps that need them.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## Secrets

- Prefer Key Vault-backed Dapr secret stores or direct Key Vault SDK reads.
- Keep component secret references out of source-controlled plaintext.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Correlate app logs and Dapr sidecar logs with trace ids and app ids.
- Export OpenTelemetry traces for service invocation and pub/sub flows.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Using Dapr for a single-component app that only needs one SDK call; direct SDK access is simpler.
- Adding Dapr before component ownership, retries, and observability are clear.
- Avoiding Dapr when cross-language eventing, state, or service invocation spans multiple ACA services; that is where it shines.
