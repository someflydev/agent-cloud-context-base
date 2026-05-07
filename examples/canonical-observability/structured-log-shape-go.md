# Structured Log Shape: Go

```go
entry := map[string]any{
  "timestamp": timestamp,
  "level": "info",
  "msg": "request completed",
  "trace_id": traceID,
  "span_id": spanID,
  "request_id": requestID,
  "correlation_id": correlationID,
  "tenant_id": tenantID,
  "dedupe_key": dedupeKey,
  "latency_ms": latencyMS,
}
```
