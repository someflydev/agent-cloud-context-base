from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any


@dataclass(frozen=True)
class AlertEvent:
    event_id: str
    subject: str
    severity: str
    resource_id: str
    operation: str


def route_alert(event: dict[str, Any]) -> dict[str, Any]:
    alert = AlertEvent(
        event_id=str(event.get("id") or event.get("event_id") or "missing"),
        subject=str(event.get("subject") or "unknown"),
        severity=str(event.get("severity") or event.get("data", {}).get("severity") or "Sev3"),
        resource_id=str(event.get("resource_id") or event.get("data", {}).get("resource_id") or "unknown"),
        operation=str(event.get("operation") or event.get("eventType") or "unknown"),
    )
    idempotency_key = sha256(f"{alert.event_id}:{alert.resource_id}".encode("utf-8")).hexdigest()
    team = "platform" if alert.severity in {"Sev0", "Sev1"} else "service-owner"
    incident = {
        "id": idempotency_key,
        "event_id": alert.event_id,
        "subject": alert.subject,
        "severity": alert.severity,
        "resource_id": alert.resource_id,
        "team": team,
        "status": "routed",
    }
    service_bus_message = {
        "topic": f"alerts-{team}",
        "message_id": idempotency_key,
        "body": incident,
    }
    return {
        "idempotency_key": idempotency_key,
        "cosmos_document": incident,
        "service_bus_message": service_bus_message,
        "log": {
            "provider": "azure",
            "service": "azure-functions",
            "example": "eventgrid-alert-router",
            "idempotency_key": idempotency_key,
        },
    }


def main(event_grid_event: dict[str, Any]) -> str:
    return json.dumps(route_alert(event_grid_event), sort_keys=True)
