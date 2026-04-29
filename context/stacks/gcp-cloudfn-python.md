# GCP Cloud Functions Python

Load this stack for Google Cloud Functions Gen2 workloads written in Python. It owns functions-framework entrypoints, Cloud Run-backed execution assumptions, CloudEvent parsing, and accb function trigger validation.

## Runtime Surface

- Runtime pin: Python 3.12 on Cloud Functions Gen2.
- Packaging: source upload by default; use containerized Cloud Run only when function packaging no longer fits.
- Dependency tool: uv preferred for generated repos; `requirements.txt` acceptable for direct Cloud Functions compatibility.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; use min instances only when latency requires the cost.
- Limits: declare timeout and memory explicitly; keep request handlers short and escalate long jobs to Cloud Run jobs or Workflows.
- Supported triggers: HTTP, Cloud Storage, Pub/Sub, Eventarc Cloud Audit Logs, other Eventarc CloudEvent sources, Firestore Native triggers, Firebase Auth, Firebase Realtime DB, Cloud Scheduler over HTTP, Workflows callbacks.

## Project Layout

```
src/<app_name>/
  main.py
  events.py
  idempotency.py
  settings.py
tests/
  fixtures/events/
  unit/
  integration/
pyproject.toml
```

## Handler Skeleton

```python
from __future__ import annotations

from cloudevents.http import CloudEvent


def handle_event(event: CloudEvent) -> None:
    event_id = event["id"]
    print({"ok": True, "event_id": event_id})
```

## Local Invocation

```bash
uv run functions-framework --target handle_event --signature-type cloudevent
uv run python -m pytest tests/integration/test_cloud_event.py
```

## Idempotency Pattern

- Derive the dedupe key from CloudEvent `id` plus `source`, GCS bucket/name/generation, Pub/Sub messageId, Firestore document path plus update time, Firebase uid plus event id, Scheduler job plus schedule time, or Workflows callback id.
- Bind dedupe records to Firestore with environment, function name, dedupe key, status, effect checksum, and TTL policy.
- Keep replay behavior aligned with `context/doctrine/idempotency-and-replay.md`.
- Replay test command: `uv run python -m pytest tests/integration/test_idempotency_replay.py`.

## Identity Binding

- Use a dedicated service account per function boundary or related trigger group.
- Grant only required roles at resource scope, not project-wide owner/editor roles.
- Reference `context/stacks/identity-gcp-iam-sa.md` for the PROMPT_12 identity stack.

## Secrets

- Use Secret Manager; bind secret access through the function service account and inject references, not plaintext values.
- Prefer runtime SDK reads for rotating credentials; environment projection is acceptable for non-sensitive names.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit structured JSON logs with `timestamp`, `severity`, `service`, `env`, `execution_id`, `event_id`, `trigger_type`, `dedupe_key`, and `outcome`.
- Propagate trace context from `traceparent`, `X-Cloud-Trace-Context`, CloudEvent extensions, or Pub/Sub attributes.
- Emit custom metrics for accepted, duplicate, retryable, and terminal events through Cloud Monitoring or OpenTelemetry.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudfn-trigger-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Depending on Gen1 behavior for a Gen2 Cloud Run-backed function.
- Using project-wide IAM roles for a single trigger.
- Treating Pub/Sub ack as safe before the durable effect is recorded.
- Running orchestration loops inside the function instead of Workflows.
