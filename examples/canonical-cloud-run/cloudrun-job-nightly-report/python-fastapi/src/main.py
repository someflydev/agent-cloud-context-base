from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None


SERVICE_NAME = "cloudrun-job-nightly-report"
app = FastAPI() if FastAPI else None


def health() -> dict[str, Any]:
    return {"ok": True, "service": SERVICE_NAME}


def ready() -> dict[str, Any]:
    return {
        "ready": True,
        "checks": ["firestore", "gcs", "pubsub", "secret-manager"],
    }


def submit(payload: dict[str, Any]) -> dict[str, Any]:
    submission_id = str(payload.get("submission_id") or "demo-submission")
    return {
        "submission_id": submission_id,
        "state_document": f"workflow/{submission_id}",
        "attachment_bucket": os.getenv("ATTACHMENT_BUCKET", "accb-dev-cloudrun-attachments"),
        "fanout_topic": os.getenv("REVIEW_TOPIC", "accb-dev-cloudrun-review"),
        "callback_target": os.getenv("WORKER_CALLBACK_URL", "http://127.0.0.1:8080/callback"),
    }


def callback(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "accepted": True,
        "iam_audience": os.getenv("CALLBACK_AUDIENCE", "private-worker"),
        "reviewer": payload.get("reviewer", "credential-from-secret-manager"),
    }


def cleanup() -> dict[str, Any]:
    return {"job": "nightly-cleanup", "expired_items_removed": 0}


if app:
    app.get("/healthz")(health)
    app.get("/readyz")(ready)
    app.get("/cleanup")(cleanup)
    app.post("/submit")(submit)
    app.post("/callback")(callback)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        routes = {
            "/healthz": health,
            "/readyz": ready,
            "/cleanup": cleanup,
        }
        route = routes.get(urlparse(self.path).path)
        if route is None:
            self.respond({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        self.respond(route())

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        payload = self.read_json()
        if path == "/submit":
            self.respond(submit(payload), HTTPStatus.ACCEPTED)
            return
        if path == "/callback":
            self.respond(callback(payload))
            return
        self.respond({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length", "0") or "0")
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def respond(self, body: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status.value)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    port = int(os.getenv("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
