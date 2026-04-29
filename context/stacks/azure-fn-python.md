# Azure Functions Python

Load this stack for Azure Functions written in Python using the v2 decorator model. It owns Core Tools v4 local execution, trigger bindings, managed identity access, and accb replay validation expectations.

## Runtime Surface

- Runtime pin: Python 3.12 where supported by Azure Functions, using the Python v2 programming model.
- Packaging: function app source package; use deployment slots and avoid hand-edited portal code.
- Dependency tool: uv preferred for generated repos; `requirements.txt` emitted for Azure Functions deployment compatibility.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; use Premium or Flex when Consumption variability violates the contract.
- Limits: declare timeout, memory plan, and concurrency; move long orchestration to Durable Functions or Container Apps jobs.
- Supported triggers: HTTP, Blob Storage, Queue Storage, Service Bus queue, Service Bus topic, Event Grid, Event Hubs, Cosmos DB Change Feed, Timer NCRONTAB, Entra External ID validation, SignalR.

## Project Layout

```
function_app.py
src/<app_name>/
  events.py
  idempotency.py
  settings.py
tests/
  fixtures/events/
  unit/
  integration/
host.json
```

## Handler Skeleton

```python
import azure.functions as func

app = func.FunctionApp()


@app.route(route="health", auth_level=func.AuthLevel.FUNCTION)
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse('{"ok":true}', mimetype="application/json")
```

## Local Invocation

```bash
func start
uv run python -m pytest tests/integration/test_function_binding.py
```

## Idempotency Pattern

- Derive the dedupe key from binding metadata: Blob url plus etag, Queue message id plus insertion time, Service Bus messageId, Event Grid id, Event Hubs sequence number plus partition, Cosmos DB item id plus `_etag`, Timer schedule time, HTTP idempotency header, or SignalR invocation id.
- Bind dedupe records to Cosmos DB with environment, function name, dedupe key, status, effect checksum, and TTL.
- Treat Entra External ID validation as an auth boundary; dedupe mutating HTTP effects after token validation.
- Replay test command: `uv run python -m pytest tests/integration/test_idempotency_replay.py`.

## Identity Binding

- Use a system-assigned or user-assigned managed identity for the function app.
- Scope role assignments to exact storage accounts, queues, topics, Cosmos containers, Key Vault secrets, and Event Grid resources.
- Reference `context/stacks/identity-azure-entra-mi.md` for the PROMPT_12 identity stack.

## Secrets

- Use Azure Key Vault with managed identity; keep app settings to secret names, vault URIs, or non-sensitive configuration.
- Prefer Key Vault references or SDK reads over plaintext settings.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit structured JSON logs with `timestamp`, `level`, `service`, `env`, `invocation_id`, `trigger_type`, `dedupe_key`, and `outcome`.
- Propagate trace context from HTTP headers, binding metadata, Service Bus application properties, Event Grid data, or Event Hubs properties.
- Emit Application Insights or OpenTelemetry metrics for accepted, duplicate, retryable, and terminal events.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `azure-fn-trigger-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Mixing v1 `function.json` authoring with v2 decorators without intent.
- Storing connection strings in source or plaintext app settings.
- Using Timer triggers for queue polling loops.
- Relying on warm process memory for replay safety.
