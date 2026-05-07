from __future__ import annotations

import json, os, time
from dataclasses import dataclass
from typing import Any, Protocol

class FirestoreClient(Protocol):
    def claim_user_event(self, dedupe_key: str, payload: dict[str, Any]) -> bool: ...
    def write_profile(self, uid: str, payload: dict[str, Any]) -> None: ...
class PubSubClient(Protocol):
    def publish(self, topic: str, payload: dict[str, Any]) -> None: ...
@dataclass
class Clients:
    firestore: FirestoreClient
    pubsub: PubSubClient

def handle_firebase_user(event: dict[str, Any], clients: Clients | None = None) -> dict[str, Any]:
    started = time.time()
    data = event.get("data", {})
    uid = data["uid"]
    email = data.get("email", "")
    event_id = event.get("id", uid)
    dedupe_key = f"{uid}:{event_id}"
    clients = clients or _gcp_clients()
    if not clients.firestore.claim_user_event(dedupe_key, data):
        _log(started, event_id, dedupe_key, "DROP", "duplicate firebase onboarding")
        return {"ok": True, "duplicate": True, "decision": "DROP"}
    profile = {"uid": uid, "email": email, "status": "ONBOARDING_STARTED"}
    clients.firestore.write_profile(uid, profile)
    clients.pubsub.publish(os.getenv("ONBOARDING_TOPIC", "accb-dev-gcp-firebase-onboarding"), profile)
    _log(started, event_id, dedupe_key, "ALLOW", "firebase onboarding started")
    return {"ok": True, "duplicate": False, "decision": "ALLOW", "profile": profile}

def _gcp_clients() -> Clients:
    raise RuntimeError("GCP clients are bound by deployment; tests inject clients.")

def _log(started: float, event_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(json.dumps({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "severity": "INFO", "msg": msg, "trace_id": os.getenv("TRACEPARENT", "local-trace"), "request_id": event_id, "correlation_id": event_id, "provider": "gcp", "runtime_tier": "function", "function_name": os.getenv("FUNCTION_TARGET", "accb-dev-gcp-firebase-onboarding"), "dedupe_key": dedupe_key, "decision": decision, "latency_ms": int((time.time() - started) * 1000)}))
