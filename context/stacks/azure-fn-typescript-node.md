# Azure Functions TypeScript Node

Load this stack for Azure Functions written in TypeScript on Node.js with the v4 programming model. It owns `@azure/functions` handler shape, Core Tools v4 local execution, trigger bindings, and accb replay validation.

## Runtime Surface

- Runtime pin: Node.js 20 with `@azure/functions` v4.
- Packaging: compiled JavaScript function app package; bundle only when the dependency graph benefits from it.
- Dependency tool: npm, pnpm, or bun follows the generated repo choice.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; use Premium or Flex when cold starts break the contract.
- Limits: declare timeout, plan, memory, and concurrency; use Durable Functions or Container Apps jobs for orchestration and long work.
- Supported triggers: HTTP, Blob Storage, Queue Storage, Service Bus queue, Service Bus topic, Event Grid, Event Hubs, Cosmos DB Change Feed, Timer NCRONTAB, Entra External ID validation, SignalR.

## Project Layout

```
src/
  functions/
    health.ts
  events.ts
  idempotency.ts
  settings.ts
tests/
  fixtures/events/
  unit/
  integration/
host.json
package.json
```

## Handler Skeleton

```typescript
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function health(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
  context.log(JSON.stringify({ ok: true, invocationId: context.invocationId }));
  return { jsonBody: { ok: true } };
}

app.http("health", { methods: ["GET"], authLevel: "function", handler: health });
```

## Local Invocation

```bash
npm test -- tests/unit
npm test -- tests/integration/function-binding.test.ts
```

## Idempotency Pattern

- Derive the dedupe key from Blob url plus etag, Queue message id plus insertion time, Service Bus messageId, Event Grid id, Event Hubs sequence number plus partition, Cosmos DB item id plus `_etag`, Timer schedule time, HTTP idempotency header, or SignalR invocation id.
- Bind dedupe records to Cosmos DB with environment, function name, dedupe key, status, effect checksum, and TTL.
- Validate Entra External ID tokens before deriving business-scoped dedupe keys for mutating HTTP requests.
- Replay test command: `npm test -- tests/integration/idempotency-replay.test.ts`.

## Identity Binding

- Use managed identity for the function app and role assignments for exact resources.
- Scope Storage, Service Bus, Event Grid, Event Hubs, Cosmos DB, SignalR, and Key Vault permissions to least privilege.
- Reference `context/stacks/identity-azure-entra-mi.md` for the PROMPT_12 identity stack.

## Secrets

- Use Azure Key Vault through managed identity; app settings may contain vault URIs or secret names, not plaintext values.
- Prefer SDK reads or Key Vault references depending on rotation and startup needs.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit JSON logs with `timestamp`, `level`, `service`, `env`, `invocationId`, `triggerType`, `dedupeKey`, and `outcome`.
- Propagate trace context from HTTP headers, binding metadata, Service Bus properties, Event Grid metadata, or Event Hubs properties.
- Emit Application Insights or OpenTelemetry metrics for accepted, duplicate, retryable, and terminal outcomes.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `azure-fn-trigger-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Mixing v3 and v4 Node programming models in one generated app.
- Relying on connection strings when managed identity is available.
- Treating Event Grid and Event Hubs payloads as the same event contract.
- Keeping dedupe state in module-level maps.
