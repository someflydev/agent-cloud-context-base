from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Protocol


class FirestoreClient(Protocol):
    def claim_generation(self, dedupe_key: str, payload: dict[str, Any]) -> bool: ...
    def write_metadata(self, dedupe_key: str, payload: dict[str, Any]) -> None: ...


class VisionClient(Protocol):
    def ocr(self, bucket: str, name: str, generation: str) -> str: ...


class PubSubClient(Protocol):
    def publish(self, topic: str, payload: dict[str, Any]) -> None: ...


@dataclass
class Clients:
    firestore: FirestoreClient
    vision: VisionClient
    pubsub: PubSubClient


def handle_gcs_object(event: dict[str, Any], clients: Clients | None = None) -> dict[str, Any]:
    started = time.time()
    data = event.get("data", {})
    bucket = data["bucket"]
    name = data["name"]
    generation = str(data.get("generation") or data.get("metageneration") or "0")
    event_id = event.get("id", f"{bucket}/{name}/{generation}")
    dedupe_key = f"{bucket}:{name}:{generation}"
    clients = clients or _gcp_clients()

    claimed = clients.firestore.claim_generation(dedupe_key, {"bucket": bucket, "name": name, "generation": generation})
    if not claimed:
        _log(started, event_id, dedupe_key, "DROP", "duplicate object generation")
        return {"ok": True, "duplicate": True, "decision": "DROP"}

    text = clients.vision.ocr(bucket, name, generation)
    payload = {"bucket": bucket, "name": name, "generation": generation, "text": text, "status": "OCR_COMPLETE"}
    clients.firestore.write_metadata(dedupe_key, payload)
    clients.pubsub.publish(os.getenv("DOWNSTREAM_TOPIC", "accb-dev-gcp-ocr-downstream"), payload)
    _log(started, event_id, dedupe_key, "ALLOW", "ocr metadata written")
    return {"ok": True, "duplicate": False, "decision": "ALLOW", "text": text}


def _gcp_clients() -> Clients:
    raise RuntimeError("GCP clients are bound by deployment; tests inject clients.")


def _log(started: float, event_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(
        json.dumps(
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "severity": "INFO",
                "msg": msg,
                "trace_id": os.getenv("TRACEPARENT", "local-trace"),
                "request_id": event_id,
                "correlation_id": event_id,
                "provider": "gcp",
                "runtime_tier": "function",
                "function_name": os.getenv("FUNCTION_TARGET", "accb-dev-gcp-ocr-handler"),
                "dedupe_key": dedupe_key,
                "decision": decision,
                "latency_ms": int((time.time() - started) * 1000),
            }
        )
    )
