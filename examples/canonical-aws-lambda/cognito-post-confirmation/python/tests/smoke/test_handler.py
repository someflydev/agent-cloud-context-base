import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from handler import lambda_handler


class FakeClients:
    def __init__(self):
        self.claimed = set()
        self.profiles = {}
        self.events = []

    def claim_user(self, user_pool_id, user_name):
        key = f"{user_pool_id}:{user_name}"
        if key in self.claimed:
            return False
        self.claimed.add(key)
        return True

    def create_profile(self, user_id, email):
        self.profiles[user_id] = email

    def publish_signup(self, detail):
        self.events.append(detail)


class HandlerSmokeTest(unittest.TestCase):
    def test_creates_profile_and_event(self):
        clients = FakeClients()
        result = lambda_handler(event(), clients=clients)
        self.assertEqual(result["userName"], "user-1")
        self.assertEqual(clients.profiles["user-1"], "user@example.com")
        self.assertEqual(len(clients.events), 1)


def event():
    return {"userPoolId": "pool-1", "userName": "user-1", "request": {"userAttributes": {"email": "user@example.com"}}}


if __name__ == "__main__":
    unittest.main()
