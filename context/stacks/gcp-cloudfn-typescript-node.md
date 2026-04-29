# GCP Cloud Functions TypeScript Node

Load this stack for Google Cloud Functions Gen2 workloads written in TypeScript on Node.js. It owns functions-framework entrypoints, tsup or esbuild bundling, CloudEvent contracts, and accb trigger validation.

## Runtime Surface

- Runtime pin: Node.js 20 on Cloud Functions Gen2.
- Packaging: source upload with compiled JavaScript; bundle with tsup or esbuild when dependency shape benefits from it.
- Dependency tool: npm, pnpm, or bun follows the generated repo choice.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; keep global initialization narrow.
- Limits: declare timeout, memory, and concurrency; use Cloud Run or Workflows when request duration or orchestration grows.
- Supported triggers: HTTP, Cloud Storage, Pub/Sub, Eventarc Cloud Audit Logs, other Eventarc CloudEvent sources, Firestore Native triggers, Firebase Auth, Firebase Realtime DB, Cloud Scheduler over HTTP, Workflows callbacks.

## Project Layout

```
src/
  index.ts
  events.ts
  idempotency.ts
  settings.ts
tests/
  fixtures/events/
  unit/
  integration/
package.json
tsconfig.json
```

## Handler Skeleton

```typescript
import type { CloudEvent } from "@google-cloud/functions-framework";
import { cloudEvent } from "@google-cloud/functions-framework";

cloudEvent("handleEvent", async (event: CloudEvent<unknown>) => {
  console.log(JSON.stringify({ ok: true, eventId: event.id }));
});
```

## Local Invocation

```bash
npm test -- tests/unit
npm test -- tests/integration/cloud-event.test.ts
```

## Idempotency Pattern

- Derive the dedupe key from CloudEvent `id` plus `source`, GCS bucket/name/generation, Pub/Sub messageId, Firestore document path plus update time, Firebase uid plus event id, Scheduler job plus schedule time, or Workflows callback id.
- Bind dedupe records to Firestore with environment, function name, dedupe key, status, effect checksum, and TTL policy.
- Keep duplicate logs and metrics distinguishable from first processing.
- Replay test command: `npm test -- tests/integration/idempotency-replay.test.ts`.

## Identity Binding

- Use a dedicated service account for each function boundary or narrow trigger group.
- Scope Pub/Sub, Firestore, GCS, Secret Manager, and Eventarc permissions to the smallest resource set.
- Reference `context/stacks/identity-gcp-iam-sa.md` for the PROMPT_12 identity stack.

## Secrets

- Use Secret Manager with service-account IAM; pass secret resource names through configuration and fetch through client libraries.
- Avoid committing `.env` files and avoid plaintext secret projection in generated examples.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-gcp-secret-manager.md`.

## Observability

- Emit JSON logs with `timestamp`, `severity`, `service`, `env`, `executionId`, `eventId`, `triggerType`, `dedupeKey`, and `outcome`.
- Propagate trace context from `traceparent`, `X-Cloud-Trace-Context`, CloudEvent extensions, or Pub/Sub attributes.
- Emit Cloud Monitoring or OpenTelemetry metrics for accepted, duplicate, retryable, and terminal outcomes.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudfn-trigger-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Treating HTTP and CloudEvent functions as interchangeable signatures.
- Shipping uncompiled TypeScript without matching deployment configuration.
- Granting broad project roles to satisfy one client call.
- Using in-memory maps for dedupe state.
