from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Protocol


class DynamoTable(Protocol):
    def put_item(self, **kwargs: Any) -> Any: ...


class RekognitionClient(Protocol):
    def detect_labels(self, **kwargs: Any) -> dict[str, Any]: ...
    def detect_moderation_labels(self, **kwargs: Any) -> dict[str, Any]: ...


class EventBridgeClient(Protocol):
    def put_events(self, **kwargs: Any) -> Any: ...


@dataclass
class Clients:
    table: DynamoTable
    rekognition: RekognitionClient
    eventbridge: EventBridgeClient


class DuplicateObjectVersion(Exception):
    pass


def lambda_handler(event: dict[str, Any], context: Any = None, clients: Clients | None = None) -> dict[str, Any]:
    started = time.time()
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    obj = record["s3"]["object"]
    key = obj["key"]
    version = obj.get("versionId") or obj.get("sequencer") or "unversioned"
    request_id = getattr(context, "aws_request_id", "local-request")
    correlation_id = record.get("responseElements", {}).get("x-amz-request-id", request_id)
    dedupe_key = f"{bucket}:{key}:{version}"
    clients = clients or _aws_clients()

    try:
        clients.table.put_item(
            Item={"pk": dedupe_key, "bucket": bucket, "object_key": key, "version": version, "status": "STARTED"},
            ConditionExpression="attribute_not_exists(pk)",
        )
    except Exception as exc:
        code = getattr(exc, "response", {}).get("Error", {}).get("Code")
        if exc.__class__.__name__ in {"ConditionalCheckFailedException", "DuplicateObjectVersion"} or code == "ConditionalCheckFailedException":
            decision = "DROP"
            _log(started, request_id, correlation_id, dedupe_key, decision, "duplicate object version")
            return {"ok": True, "duplicate": True, "decision": decision}
        raise

    labels = clients.rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    moderation = clients.rekognition.detect_moderation_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    flagged = bool(moderation.get("ModerationLabels"))
    decision = "FLAG" if flagged else "ALLOW"
    if flagged:
        clients.eventbridge.put_events(
            Entries=[
                {
                    "Source": "accb.s3mod",
                    "DetailType": "ImageModerationDecision",
                    "Detail": json.dumps({"bucket": bucket, "key": key, "version": version, "decision": decision}),
                    "EventBusName": os.getenv("EVENT_BUS_NAME", "accb-dev-s3mod-events"),
                }
            ]
        )
    clients.table.put_item(Item={"pk": dedupe_key, "status": decision, "labels": labels.get("Labels", [])})
    _log(started, request_id, correlation_id, dedupe_key, decision, "moderation complete")
    return {"ok": True, "duplicate": False, "decision": decision}


def _aws_clients() -> Clients:
    import boto3

    return Clients(
        table=boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]),
        rekognition=boto3.client("rekognition"),
        eventbridge=boto3.client("events"),
    )


def _log(started: float, request_id: str, correlation_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(
        json.dumps(
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "level": "INFO",
                "msg": msg,
                "trace_id": os.getenv("_X_AMZN_TRACE_ID", "local-trace"),
                "request_id": request_id,
                "correlation_id": correlation_id,
                "provider": "aws",
                "runtime_tier": "function",
                "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "accb-dev-s3mod-handler"),
                "dedupe_key": dedupe_key,
                "decision": decision,
                "latency_ms": int((time.time() - started) * 1000),
            }
        )
    )
