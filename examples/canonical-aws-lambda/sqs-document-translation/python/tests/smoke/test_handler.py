import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from handler import lambda_handler


class FakeClients:
    def __init__(self):
        self.claimed = set()
        self.artifacts = {}

    def claim(self, key):
        if key in self.claimed:
            return False
        self.claimed.add(key)
        return True

    def get_object(self, bucket, key):
        return "hello"

    def translate(self, text, source_lang, target_lang):
        return f"{text}:{target_lang}"

    def put_object(self, bucket, key, body):
        self.artifacts[f"{bucket}/{key}"] = body

    def complete(self, key, status):
        pass


class HandlerSmokeTest(unittest.TestCase):
    def test_translates_document(self):
        clients = FakeClients()
        result = lambda_handler(event("msg_1"), clients=clients)
        self.assertEqual(result["processed"], 1)
        self.assertEqual(clients.artifacts["dest/out.txt"], "hello:es")


def event(message_id):
    body = {"source_bucket": "source", "source_key": "in.txt", "dest_bucket": "dest", "dest_key": "out.txt", "source_lang": "en", "target_lang": "es"}
    return {"Records": [{"messageId": message_id, "body": json.dumps(body)}]}


if __name__ == "__main__":
    unittest.main()
