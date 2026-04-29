# Azure Container Apps Jobs

Load this stack for Azure Container Apps Jobs used for manual, scheduled, or event-driven container tasks. It owns job trigger shape, scaling rules, retry behavior, and accb container validation.

## Image Surface

- Runtime pin: language-specific, with the final image deployed by digest.
- Registry: Azure Container Registry with git SHA tags and immutable promotion.
- Base image: digest-pinned slim, distroless, or chiseled runtime image.
- Build: multi-stage Dockerfile with build tooling removed from the final stage.
- User: run as non-root and write only to declared temp paths.
- Security: produce an SBOM and scan before promotion.

## Service Surface

- Entrypoint: a bounded command that exits 0 on success and non-zero on failure.
- Health paths are not HTTP probes; use execution status, logs, and completion metrics.
- Concurrency: declare parallelism, replica completions, and KEDA event scale rules.
- Scaling: jobs support manual, scheduled, and event triggers with retry and timeout settings.
- Startup: account for image pull and dependency initialization inside execution timeout.
- Triggers: manual, cron scheduled, Service Bus, Event Hubs, queues, and custom KEDA scalers.

## Networking

- Jobs run inside a Container Apps environment with the same external or internal network model.
- Use VNet integration for private storage, databases, queues, or internal endpoints.
- Declare private DNS, egress, and firewall expectations.
- Bound parallel jobs to avoid exhausting database connections or private endpoints.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
src/<job_name>/
  job_entrypoint.*
  settings.*
  telemetry.*
tests/
  unit/
  integration/
Dockerfile
```

## Local Run

```bash
docker build -t <job_name>:dev .
docker run --rm -e ACCB_ENV=dev <job_name>:dev
```

## Idempotency Pattern

- Derive replay keys from schedule time, event message identity, input object, or job execution id plus replica index.
- Store durable progress and effect checksums before acknowledging source events.
- Make retries resume completed work or no-op safely.

## Identity Binding

- Use managed identity for ACR, Key Vault, event sources, storage, and data stores.
- Scope RBAC to exact job inputs and outputs.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## Secrets

- Use Key Vault references or SDK reads through managed identity.
- Do not pass credentials as command arguments or image build args.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit logs with `job`, `execution`, `replica`, `attempt`, `env`, and `outcome`.
- Export processed item count, retry count, duration, and terminal failure metrics.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Running unbounded daemons as jobs.
- Ignoring retry semantics for event-triggered jobs.
- Scaling parallel jobs beyond downstream capacity.
