import os
import pathlib
import json
import subprocess
import sys
from typing import Any

example_root = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(example_root / "src"))

from handler import Clients, lambda_handler


class Rekognition:
    def detect_labels(self, **kwargs):
        return {"Labels": [{"Name": "Document"}]}

    def detect_moderation_labels(self, **kwargs):
        return {"ModerationLabels": [{"Name": "Explicit Nudity"}]}


class Events:
    def __init__(self):
        self.entries = []

    def put_events(self, **kwargs):
        self.entries.extend(kwargs["Entries"])


class ConditionalCheckFailedException(Exception):
    def __init__(self):
        self.response = {"Error": {"Code": "ConditionalCheckFailedException"}}


class MiniStackDynamoTable:
    def __init__(self, table_name):
        self.table_name = table_name

    def put_item(self, **kwargs):
        command = [
            "docker",
            "compose",
            "exec",
            "-T",
            "ministack",
            "awslocal",
            "dynamodb",
            "put-item",
            "--table-name",
            self.table_name,
            "--item",
            json.dumps({key: dynamodb_value(value) for key, value in kwargs["Item"].items()}),
        ]
        if kwargs.get("ConditionExpression"):
            command.extend(["--condition-expression", kwargs["ConditionExpression"]])
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode == 0:
            return None
        if "ConditionalCheckFailed" in result.stderr:
            raise ConditionalCheckFailedException()
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def dynamodb_value(value: Any) -> dict[str, Any]:
    if isinstance(value, str):
        return {"S": value}
    if isinstance(value, bool):
        return {"BOOL": value}
    if isinstance(value, (int, float)):
        return {"N": str(value)}
    if isinstance(value, list):
        return {"L": [dynamodb_value(item) for item in value]}
    if isinstance(value, dict):
        return {"M": {key: dynamodb_value(item) for key, item in value.items()}}
    if value is None:
        return {"NULL": True}
    raise TypeError(f"unsupported DynamoDB value: {value!r}")


def event(version):
    return {"Records": [{"s3": {"bucket": {"name": "accb-dev-s3mod-images"}, "object": {"key": "lane-a.jpg", "versionId": version}}}]}


def main():
    table_name = os.environ.get("TABLE_NAME", "accb-dev-s3mod-records")
    table = MiniStackDynamoTable(table_name)
    clients = Clients(table=table, rekognition=Rekognition(), eventbridge=Events())
    first = lambda_handler(event("lane-a-v1"), clients=clients)
    second = lambda_handler(event("lane-a-v1"), clients=clients)
    assert first["duplicate"] is False
    assert second["duplicate"] is True


if __name__ == "__main__":
    main()
