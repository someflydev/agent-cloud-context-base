from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Protocol


class ClientsProtocol(Protocol):
    def claim(self, key: str) -> bool: ...
    def get_object(self, bucket: str, key: str) -> str: ...
    def translate(self, text: str, source_lang: str, target_lang: str) -> str: ...
    def put_object(self, bucket: str, key: str, body: str) -> None: ...
    def complete(self, key: str, status: str) -> None: ...


@dataclass
class Clients:
    s3: Any
    table: Any
    translate_client: Any

    def claim(self, key: str) -> bool:
        try:
            self.table.put_item(Item={"pk": key, "status": "STARTED"}, ConditionExpression="attribute_not_exists(pk)")
            return True
        except Exception as exc:
            code = getattr(exc, "response", {}).get("Error", {}).get("Code")
            if exc.__class__.__name__ == "ConditionalCheckFailedException" or code == "ConditionalCheckFailedException":
                return False
            raise

    def get_object(self, bucket: str, key: str) -> str:
        return self.s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        return self.translate_client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)["TranslatedText"]

    def put_object(self, bucket: str, key: str, body: str) -> None:
        self.s3.put_object(Bucket=bucket, Key=key, Body=body.encode())

    def complete(self, key: str, status: str) -> None:
        self.table.put_item(Item={"pk": key, "status": status})


def lambda_handler(event: dict[str, Any], context: Any = None, clients: ClientsProtocol | None = None) -> dict[str, Any]:
    started = time.time()
    clients = clients or _aws_clients()
    processed = 0
    duplicates = 0
    for record in event["Records"]:
        if context and hasattr(context, "get_remaining_time_in_millis") and context.get_remaining_time_in_millis() < 5000:
            raise TimeoutError("visibility-timeout guard: insufficient time remains")
        message_id = record["messageId"]
        job = json.loads(record["body"])
        if not clients.claim(message_id):
            duplicates += 1
            _log(started, message_id, message_id, "DROP", "duplicate message")
            continue
        source = clients.get_object(job["source_bucket"], job["source_key"])
        translated = clients.translate(source, job["source_lang"], job["target_lang"])
        clients.put_object(job["dest_bucket"], job["dest_key"], translated)
        clients.complete(message_id, "COMPLETED")
        processed += 1
        _log(started, message_id, message_id, "ALLOW", "translation complete")
    return {"ok": True, "processed": processed, "duplicates": duplicates}


def _aws_clients() -> Clients:
    import boto3

    return Clients(
        s3=boto3.client("s3"),
        table=boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]),
        translate_client=boto3.client("translate"),
    )


def _log(started: float, request_id: str, dedupe_key: str, decision: str, msg: str) -> None:
    print(json.dumps({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": "INFO",
        "msg": msg,
        "trace_id": os.getenv("_X_AMZN_TRACE_ID", "local-trace"),
        "request_id": request_id,
        "correlation_id": request_id,
        "provider": "aws",
        "runtime_tier": "function",
        "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "accb-dev-translate-handler"),
        "dedupe_key": dedupe_key,
        "decision": decision,
        "latency_ms": int((time.time() - started) * 1000),
    }))
