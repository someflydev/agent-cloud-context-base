"""FastAPI ingest role for the accb rag-asset-pipeline Kubernetes example."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="accb rag-asset-pipeline api")


class Event(BaseModel):
    id: str
    source: str = "local"


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
def ingest(event: Event) -> dict[str, str]:
    return {
        "event_id": event.id,
        "source": event.source,
        "status": "queued",
        "accepted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
