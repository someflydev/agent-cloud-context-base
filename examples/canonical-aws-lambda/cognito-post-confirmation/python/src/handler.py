from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Protocol


class ClientsProtocol(Protocol):
    def claim_user(self, user_pool_id: str, user_name: str) -> bool: ...
    def create_profile(self, user_id: str, email: str) -> None: ...
    def publish_signup(self, detail: dict[str, str]) -> None: ...


@dataclass
class Clients:
    table: Any
    eventbridge: Any

    def claim_user(self, user_pool_id: str, user_name: str) -> bool:
        try:
            self.table.put_item(Item={"pk": f"{user_pool_id}:{user_name}", "status": "STARTED"}, ConditionExpression="attribute_not_exists(pk)")
            return True
        except Exception as exc:
            code = getattr(exc, "response", {}).get("Error", {}).get("Code")
            if exc.__class__.__name__ == "ConditionalCheckFailedException" or code == "ConditionalCheckFailedException":
                return False
            raise

    def create_profile(self, user_id: str, email: str) -> None:
        self.table.put_item(Item={"pk": f"profile:{user_id}", "email": email, "status": "ACTIVE"})

    def publish_signup(self, detail: dict[str, str]) -> None:
        self.eventbridge.put_events(Entries=[{"Source": "accb.cognito", "DetailType": "UserConfirmed", "Detail": json.dumps(detail), "EventBusName": os.getenv("EVENT_BUS_NAME", "accb-dev-cognito-events")}])


def lambda_handler(event: dict[str, Any], context: Any = None, clients: ClientsProtocol | None = None) -> dict[str, Any]:
    started = time.time()
    request_id = getattr(context, "aws_request_id", "local-request")
    user_pool_id = event["userPoolId"]
    user_name = event["userName"]
    attrs = event.get("request", {}).get("userAttributes", {})
    email = attrs.get("email", "")
    dedupe_key = f"{user_pool_id}:{user_name}"
    clients = clients or _aws_clients()
    if not clients.claim_user(user_pool_id, user_name):
        _log(started, request_id, dedupe_key, "DROP", "duplicate confirmation")
        return event
    clients.create_profile(user_name, email)
    clients.publish_signup({"user_pool_id": user_pool_id, "user_name": user_name, "email": email})
    _log(started, request_id, dedupe_key, "ALLOW", "post confirmation complete")
    return event


def _aws_clients() -> Clients:
    import boto3

    return Clients(table=boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]), eventbridge=boto3.client("events"))


def _log(started: float, request_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(json.dumps({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": "INFO",
        "msg": msg,
        "trace_id": os.getenv("_X_AMZN_TRACE_ID", "local-trace"),
        "request_id": request_id,
        "correlation_id": dedupe_key,
        "provider": "aws",
        "runtime_tier": "function",
        "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "accb-dev-cognito-handler"),
        "dedupe_key": dedupe_key,
        "decision": decision,
        "latency_ms": int((time.time() - started) * 1000),
    }))
