import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "smoke"))

from handler import lambda_handler
from test_handler import FakeClients, event


class ReplayTest(unittest.TestCase):
    def test_same_message_writes_one_artifact(self):
        clients = FakeClients()
        first = lambda_handler(event("msg_replay"), clients=clients)
        second = lambda_handler(event("msg_replay"), clients=clients)
        self.assertEqual(first["processed"], 1)
        self.assertEqual(second["duplicates"], 1)
        self.assertEqual(len(clients.artifacts), 1)


if __name__ == "__main__":
    unittest.main()
