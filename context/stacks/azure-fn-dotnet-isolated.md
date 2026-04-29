# Azure Functions .NET Isolated

Load this stack for Azure Functions written in .NET 8 using the isolated worker model. It owns isolated-process startup, binding contracts, managed identity access, and accb replay validation for Azure function workloads.

## Runtime Surface

- Runtime pin: .NET 8 isolated worker on Azure Functions.
- Packaging: published function app artifact from `dotnet publish`; deployment slots preferred for promotion.
- Dependency tool: .NET SDK and NuGet lock discipline from the generated repo.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; use Premium or Flex when Consumption startup is too variable.
- Limits: declare timeout, hosting plan, memory, and concurrency; use Durable Functions or Container Apps jobs for long orchestration.
- Supported triggers: HTTP, Blob Storage, Queue Storage, Service Bus queue, Service Bus topic, Event Grid, Event Hubs, Cosmos DB Change Feed, Timer NCRONTAB, Entra External ID validation, SignalR.

## Project Layout

```
src/FunctionApp/
  Program.cs
  Functions/HealthFunction.cs
  Events/
  Idempotency/
  Settings/
tests/FunctionApp.Tests/
host.json
```

## Handler Skeleton

```csharp
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;

public sealed class HealthFunction
{
    [Function("health")]
    public HttpResponseData Run([HttpTrigger(AuthorizationLevel.Function, "get")] HttpRequestData req)
    {
        var response = req.CreateResponse(System.Net.HttpStatusCode.OK);
        response.WriteString("{\"ok\":true}");
        return response;
    }
}
```

## Local Invocation

```bash
dotnet test
func start --csharp
```

## Idempotency Pattern

- Derive the dedupe key from Blob url plus etag, Queue message id plus insertion time, Service Bus messageId, Event Grid id, Event Hubs sequence number plus partition, Cosmos DB item id plus `_etag`, Timer schedule time, HTTP idempotency header, or SignalR invocation id.
- Bind dedupe records to Cosmos DB with environment, function name, dedupe key, status, effect checksum, and TTL.
- Validate Entra External ID tokens before mutating effects and include tenant or subject scope in business keys.
- Replay test command: `dotnet test --filter IdempotencyReplay`.

## Identity Binding

- Use system-assigned or user-assigned managed identity for the function app.
- Scope Azure RBAC assignments to exact Storage, Service Bus, Event Grid, Event Hubs, Cosmos DB, SignalR, and Key Vault resources.
- Reference `context/stacks/identity-azure-entra-mi.md` for the PROMPT_12 identity stack.

## Secrets

- Use Azure Key Vault with managed identity; bind options to vault URIs or secret names rather than plaintext.
- Prefer Azure SDK clients with `DefaultAzureCredential` in deployed runtime.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-azure-key-vault.md`.

## Observability

- Emit structured JSON logs with `timestamp`, `level`, `service`, `env`, `invocation_id`, `trigger_type`, `dedupe_key`, and `outcome`.
- Propagate trace context from HTTP headers, binding metadata, Service Bus application properties, Event Grid metadata, or Event Hubs properties.
- Emit Application Insights or OpenTelemetry metrics for accepted, duplicate, retryable, and terminal outcomes.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `azure-fn-trigger-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Using the in-process .NET model for new generated repos.
- Reading Key Vault through shared connection strings instead of managed identity.
- Combining unrelated triggers into one class without a clear boundary.
- Treating isolated worker startup success as proof that bindings were exercised.
