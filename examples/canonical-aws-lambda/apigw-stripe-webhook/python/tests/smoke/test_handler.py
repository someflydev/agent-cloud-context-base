import hashlib
import hmac
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from handler import lambda_handler


class FakeClients:
    def __init__(self):
        self.stored = set()
        self.workflows = []

    def get_signing_secret(self):
        return "local-signing-secret"

    def store_raw_event(self, event_id, payload):
        if event_id in self.stored:
            return False
        self.stored.add(event_id)
        return True

    def start_workflow(self, event_id, payload):
        self.workflows.append(event_id)


class HandlerSmokeTest(unittest.TestCase):
    def test_accepts_signed_webhook(self):
        clients = FakeClients()
        result = lambda_handler(event("evt_1"), clients=clients)
        self.assertEqual(result["statusCode"], 202)
        self.assertEqual(clients.workflows, ["evt_1"])


def event(event_id):
    body = json.dumps({"id": event_id, "type": "checkout.session.completed"})
    signature = hmac.new(b"local-signing-secret", body.encode(), hashlib.sha256).hexdigest()
    return {"body": body, "headers": {"stripe-signature": f"v1={signature}"}, "requestContext": {"requestId": "req_1"}}


if __name__ == "__main__":
    unittest.main()
