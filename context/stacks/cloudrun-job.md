# Cloud Run Job

Load this stack for Google Cloud Run Jobs used for one-shot, scheduled, or batch tasks. It owns container job shape, retry semantics, parallelism, and accb container validation.

## Image Surface

- Runtime pin: language-specific, but the job image must be digest-pinned at deploy time.
- Registry: Artifact Registry with git SHA tags and digest promotion.
- Base image: distroless or slim final image appropriate to the language runtime.
- Build: multi-stage Dockerfile with build tools removed from the final image.
- User: run as non-root and write only to declared temp paths.
- Security: generate an SBOM and scan before test promotion.

## Service Surface

- Entrypoint: a bounded command that exits 0 on success and non-zero on retryable or terminal failure.
- Health paths are not request probes; use startup logging and job completion status instead.
- Concurrency: model with task count and parallelism, not HTTP request concurrency.
- Scaling: declare task count, parallelism, max retries, timeout, CPU, memory, and schedule when used.
- Startup: jobs may accept slower startup, but image pull and init time still count against task runtime.
- Triggers: manual execution, Cloud Scheduler, Workflows, or event-driven orchestration that starts the job.

## Networking

- Default egress is public unless restricted by Cloud Run network settings.
- Attach VPC egress only when the job reaches a named private resource.
- Declare whether parallel tasks share a private database, queue, or storage target.
- Bound outbound fan-out to avoid private endpoint or NAT exhaustion.
- Reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
src/<app_name>/
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

- Derive the replay key from job name, execution id, task index, input object, or schedule time.
- Store per-task progress in durable storage before acknowledging external effects.
- Make retries resume work or no-op completed effects.

## Identity Binding

- Use a dedicated Cloud Run job service account.
- Grant only the batch inputs, outputs, secrets, and eventing permissions required by the job.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## Secrets

- Use Secret Manager bindings or runtime reads through the service account.
- Never pass credentials as build args or image labels.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit structured logs with `job`, `execution`, `task_index`, `attempt`, `env`, and `outcome`.
- Export duration, completed item count, retry count, and terminal failure metrics.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Running endless daemons as jobs.
- Treating parallel task retries as exactly-once without a durable progress record.
- Scheduling jobs without a bounded timeout and retry policy.
