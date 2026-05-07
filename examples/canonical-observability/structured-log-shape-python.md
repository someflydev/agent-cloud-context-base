# Structured Log Shape: Python

Emit one JSON object per line with this field set:

```python
log = {
    "timestamp": now_iso,
    "level": "INFO",
    "msg": "request completed",
    "trace_id": trace_id,
    "span_id": span_id,
    "request_id": request_id,
    "correlation_id": correlation_id,
    "tenant_id": tenant_id,
    "dedupe_key": dedupe_key,
    "latency_ms": latency_ms,
}
```
