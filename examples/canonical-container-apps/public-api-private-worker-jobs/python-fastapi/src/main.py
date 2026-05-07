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


SERVICE_NAME = "aca-public-api-private-worker-jobs"
app = FastAPI() if FastAPI else None


def health() -> dict[str, Any]:
    return {"ok": True, "service": SERVICE_NAME}


def ready() -> dict[str, Any]:
    return {
        "ready": True,
        "checks": ["cosmos", "blob-storage", "service-bus", "key-vault", "managed-identity"],
    }


def submit(payload: dict[str, Any]) -> dict[str, Any]:
    submission_id = str(payload.get("submission_id") or "demo-submission")
    return {
        "submission_id": submission_id,
        "state_container": os.getenv("COSMOS_CONTAINER", "workflow"),
        "attachment_container": os.getenv("ATTACHMENT_CONTAINER", "attachments"),
        "work_queue": os.getenv("SERVICEBUS_QUEUE", "accb-dev-aca-work"),
        "worker_url": os.getenv("WORKER_URL", "http://worker.internal/process"),
        "scale_signal": "keda-servicebus-queue-depth",
    }


def process(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "accepted": True,
        "internal_ingress": True,
        "message_id": payload.get("message_id", "local-message"),
        "secret_ref": os.getenv("API_SECRET_NAME", "keyvaultref:api-key"),
    }


def retry_batch() -> dict[str, Any]:
    return {
        "job": "servicebus-batch-retry",
        "trigger": "servicebus",
        "keda_rule": "queueLength >= 5",
        "retried": 0,
    }


if app:
    app.get("/healthz")(health)
    app.get("/readyz")(ready)
    app.get("/retry")(retry_batch)
    app.post("/submit")(submit)
    app.post("/process")(process)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        routes = {
            "/healthz": health,
            "/readyz": ready,
            "/retry": retry_batch,
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
        if path == "/process":
            self.respond(process(payload))
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
