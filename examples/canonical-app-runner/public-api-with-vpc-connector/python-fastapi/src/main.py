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


SERVICE_NAME = "public-api-with-vpc-connector"
app = FastAPI() if FastAPI else None


def health() -> dict[str, Any]:
    return {"ok": True, "service": SERVICE_NAME}


def ready() -> dict[str, Any]:
    return {
        "ready": True,
        "database_host": os.getenv("DB_HOST", "private-aurora.internal"),
        "secret_path": os.getenv("DB_SECRET_PATH", "/accb/dev/apprunner/db"),
    }


def suppliers(payload: dict[str, Any]) -> dict[str, Any]:
    supplier_id = str(payload.get("supplier_id") or "demo-supplier")
    return {
        "supplier_id": supplier_id,
        "db_operation": "insert",
        "connectivity": "app-runner-vpc-connector",
    }


if app:
    app.get("/healthz")(health)
    app.get("/readyz")(ready)
    app.post("/suppliers")(suppliers)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if urlparse(self.path).path == "/healthz":
            self.respond(health())
            return
        if urlparse(self.path).path == "/readyz":
            self.respond(ready())
            return
        self.respond({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if urlparse(self.path).path == "/suppliers":
            self.respond(suppliers(self.read_json()), HTTPStatus.ACCEPTED)
            return
        self.respond({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length", "0") or "0")
        return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}

    def respond(self, body: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status.value)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    ThreadingHTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()


if __name__ == "__main__":
    main()
