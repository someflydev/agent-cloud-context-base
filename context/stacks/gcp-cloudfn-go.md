# GCP Cloud Functions Go

Load this stack for Google Cloud Functions Gen2 workloads written in Go. It owns Go 1.22 functions-framework usage, CloudEvent handling, local invocation, and accb replay validation expectations.

## Runtime Surface

- Runtime pin: Go 1.22 on Cloud Functions Gen2.
- Packaging: source upload using Go modules; move to Cloud Run container when native binaries or custom runtime shape dominate.
- Dependency tool: Go modules.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; keep package init lightweight.
- Limits: declare timeout, memory, and concurrency; escalate long orchestration to Workflows or Cloud Run jobs.
- Supported triggers: HTTP, Cloud Storage, Pub/Sub, Eventarc Cloud Audit Logs, other Eventarc CloudEvent sources, Firestore Native triggers, Firebase Auth, Firebase Realtime DB, Cloud Scheduler over HTTP, Workflows callbacks.

## Project Layout

```
function.go
internal/events/
internal/idempotency/
internal/settings/
tests/fixtures/events/
go.mod
go.sum
```

## Handler Skeleton

```go
package function

import (
	"context"
	"log/slog"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/cloudevents/sdk-go/v2/event"
)

func init() {
	functions.CloudEvent("HandleEvent", HandleEvent)
}

func HandleEvent(ctx context.Context, e event.Event) error {
	slog.Info("event accepted", "event_id", e.ID())
	return nil
}
```

## Local Invocation

```bash
go test ./...
go test ./internal/idempotency -run Replay
```

## Idempotency Pattern

- Derive the dedupe key from CloudEvent `id` plus `source`, GCS bucket/name/generation, Pub/Sub messageId, Firestore document path plus update time, Firebase uid plus event id, Scheduler job plus schedule time, or Workflows callback id.
- Bind dedupe records to Firestore with environment, function name, dedupe key, status, effect checksum, and TTL policy.
- Keep context cancellation separate from duplicate classification.
- Replay test command: `go test ./... -run IdempotencyReplay`.

## Identity Binding

- Use a dedicated service account per function boundary or tightly related trigger group.
- Scope IAM roles to exact Pub/Sub topics, Firestore databases, GCS buckets, Secret Manager secrets, and Eventarc resources.
- Reference `context/stacks/identity-gcp-iam-sa.md` for the PROMPT_12 identity stack.

## Secrets

- Use Secret Manager; resolve secret versions through the Secret Manager client under the function service account.
- Cache clients globally; cache values only within rotation tolerance.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit structured JSON logs with `timestamp`, `severity`, `service`, `env`, `execution_id`, `event_id`, `trigger_type`, `dedupe_key`, and `outcome`.
- Propagate trace context from context values, `traceparent`, `X-Cloud-Trace-Context`, CloudEvent extensions, or Pub/Sub attributes.
- Emit Cloud Monitoring or OpenTelemetry metrics for accepted, duplicate, retryable, and terminal outcomes.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudfn-trigger-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Depending on package-level mutable state for correctness.
- Parsing every event through `map[string]any` when CloudEvent data structs are known.
- Granting project-wide editor roles to the service account.
- Hiding long-running work inside a Gen2 function instead of escalating tiers.
