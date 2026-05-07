from __future__ import annotations

import json, os, time
from dataclasses import dataclass
from typing import Any, Protocol

class FirestoreClient(Protocol):
    def claim_message(self, dedupe_key: str, payload: dict[str, Any]) -> bool: ...
    def write_translation(self, dedupe_key: str, payload: dict[str, Any]) -> None: ...
class TranslateClient(Protocol):
    def translate(self, text: str, target_locale: str) -> str: ...
class PubSubClient(Protocol):
    def publish(self, topic: str, payload: dict[str, Any]) -> None: ...
@dataclass
class Clients:
    firestore: FirestoreClient
    translate: TranslateClient
    pubsub: PubSubClient

def handle_pubsub_message(event: dict[str, Any], clients: Clients | None = None) -> dict[str, Any]:
    started = time.time()
    data = event.get("data", {})
    message_id = data["messageId"]
    target_locale = data.get("targetLocale", "es")
    text = data["text"]
    event_id = event.get("id", message_id)
    dedupe_key = f"{message_id}:{target_locale}"
    clients = clients or _gcp_clients()
    if not clients.firestore.claim_message(dedupe_key, data):
        _log(started, event_id, dedupe_key, "DROP", "duplicate pubsub translation")
        return {"ok": True, "duplicate": True, "decision": "DROP"}
    translated = clients.translate.translate(text, target_locale)
    payload = {"message_id": message_id, "target_locale": target_locale, "translated_text": translated, "status": "TRANSLATED"}
    clients.firestore.write_translation(dedupe_key, payload)
    clients.pubsub.publish(os.getenv("COMPLETION_TOPIC", "accb-dev-gcp-translation-complete"), payload)
    _log(started, event_id, dedupe_key, "ALLOW", "translation completed")
    return {"ok": True, "duplicate": False, "decision": "ALLOW", "translated_text": translated}

def _gcp_clients() -> Clients:
    raise RuntimeError("GCP clients are bound by deployment; tests inject clients.")

def _log(started: float, event_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(json.dumps({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "severity": "INFO", "msg": msg, "trace_id": os.getenv("TRACEPARENT", "local-trace"), "request_id": event_id, "correlation_id": event_id, "provider": "gcp", "runtime_tier": "function", "function_name": os.getenv("FUNCTION_TARGET", "accb-dev-gcp-pubsub-translation-stream"), "dedupe_key": dedupe_key, "decision": decision, "latency_ms": int((time.time() - started) * 1000)}))
