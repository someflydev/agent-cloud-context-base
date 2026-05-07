"""Minimal cronjob role for the accb rag-asset-pipeline Kubernetes example."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone


ROLE = "cronjob"


def handle(event: dict | None = None) -> dict:
    payload = event or {}
    event_id = payload.get("id", "sample-event")
    return {
        "role": ROLE,
        "event_id": event_id,
        "status": "accepted",
        "environment": os.getenv("ACCB_ENV", "dev"),
        "handled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main() -> None:
    print(json.dumps(handle({"id": os.getenv("ACCB_EVENT_ID", "local")})))


if __name__ == "__main__":
    main()
