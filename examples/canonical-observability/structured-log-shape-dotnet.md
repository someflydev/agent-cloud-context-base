# Structured Log Shape: .NET

```csharp
logger.LogInformation("{@Log}", new {
    timestamp,
    level = "info",
    msg = "request completed",
    trace_id,
    span_id,
    request_id,
    correlation_id,
    tenant_id,
    dedupe_key,
    latency_ms
});
```
