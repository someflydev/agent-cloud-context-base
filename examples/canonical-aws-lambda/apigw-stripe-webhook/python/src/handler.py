from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Protocol


class ClientsProtocol(Protocol):
    def get_signing_secret(self) -> str: ...
    def store_raw_event(self, event_id: str, payload: dict[str, Any]) -> bool: ...
    def start_workflow(self, event_id: str, payload: dict[str, Any]) -> None: ...


@dataclass
class Clients:
    secrets: Any
    table: Any
    stepfunctions: Any

    def get_signing_secret(self) -> str:
        return self.secrets.get_secret_value(SecretId=os.environ["STRIPE_SECRET"])["SecretString"]

    def store_raw_event(self, event_id: str, payload: dict[str, Any]) -> bool:
        try:
            self.table.put_item(Item={"pk": event_id, "payload": payload}, ConditionExpression="attribute_not_exists(pk)")
            return True
        except Exception as exc:
            code = getattr(exc, "response", {}).get("Error", {}).get("Code")
            if exc.__class__.__name__ == "ConditionalCheckFailedException" or code == "ConditionalCheckFailedException":
                return False
            raise

    def start_workflow(self, event_id: str, payload: dict[str, Any]) -> None:
        self.stepfunctions.start_execution(stateMachineArn=os.environ["WORKFLOW_ARN"], name=event_id, input=json.dumps(payload))


def lambda_handler(event: dict[str, Any], context: Any = None, clients: ClientsProtocol | None = None) -> dict[str, Any]:
    started = time.time()
    body = event.get("body") or "{}"
    payload = json.loads(body)
    event_id = payload["id"]
    request_id = event.get("requestContext", {}).get("requestId") or getattr(context, "aws_request_id", "local-request")
    clients = clients or _aws_clients()
    secret = clients.get_signing_secret()
    if not verify_stripe_signature(body, event.get("headers", {}).get("stripe-signature"), secret):
        _log(started, request_id, event_id, event_id, "DROP", "invalid stripe signature")
        return {"statusCode": 400, "body": "invalid signature"}
    inserted = clients.store_raw_event(event_id, payload)
    if inserted:
        clients.start_workflow(event_id, payload)
    _log(started, request_id, event_id, event_id, "ALLOW" if inserted else "DROP", "accepted" if inserted else "duplicate")
    return {"statusCode": 202, "body": json.dumps({"accepted": True, "duplicate": not inserted})}


def verify_stripe_signature(body: str, signature: str | None, secret: str) -> bool:
    if not signature:
        return False
    expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    return expected in signature


def _aws_clients() -> Clients:
    import boto3

    return Clients(
        secrets=boto3.client("secretsmanager"),
        table=boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]),
        stepfunctions=boto3.client("stepfunctions"),
    )


def _log(started: float, request_id: str, correlation_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(json.dumps({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": "INFO",
        "msg": msg,
        "trace_id": os.getenv("_X_AMZN_TRACE_ID", "local-trace"),
        "request_id": request_id,
        "correlation_id": correlation_id,
        "provider": "aws",
        "runtime_tier": "function",
        "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "accb-dev-stripe-handler"),
        "dedupe_key": dedupe_key,
        "decision": decision,
        "latency_ms": int((time.time() - started) * 1000),
    }))
