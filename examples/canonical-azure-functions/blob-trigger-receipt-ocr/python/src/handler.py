from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any


@dataclass(frozen=True)
class BlobEvent:
    name: str
    version: str
    content_type: str
    bytes_len: int


def process_blob(event: dict[str, Any]) -> dict[str, Any]:
    blob = BlobEvent(
        name=str(event["name"]),
        version=str(event.get("version") or event.get("etag") or "noversion"),
        content_type=str(event.get("content_type") or "application/octet-stream"),
        bytes_len=int(event.get("bytes_len") or 0),
    )
    idempotency_key = sha256(f"{blob.name}:{blob.version}".encode("utf-8")).hexdigest()
    receipt = {
        "id": idempotency_key,
        "blob_name": blob.name,
        "blob_version": blob.version,
        "merchant": event.get("merchant", "unknown"),
        "total": float(event.get("total", 0)),
        "currency": event.get("currency", "USD"),
        "ocr_status": "completed",
    }
    event_grid = {
        "eventType": "accb.receipt.ocr.completed",
        "subject": blob.name,
        "data": {"receipt_id": idempotency_key, "blob_version": blob.version},
    }
    return {
        "idempotency_key": idempotency_key,
        "cosmos_document": receipt,
        "event_grid_event": event_grid,
        "log": {
            "provider": "azure",
            "service": "azure-functions",
            "example": "blob-trigger-receipt-ocr",
            "idempotency_key": idempotency_key,
        },
    }


def main(blob_event: dict[str, Any]) -> str:
    return json.dumps(process_blob(blob_event), sort_keys=True)

