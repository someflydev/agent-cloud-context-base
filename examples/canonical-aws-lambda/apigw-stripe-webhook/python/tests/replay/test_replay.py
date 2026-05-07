import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "smoke"))

from handler import lambda_handler
from test_handler import FakeClients, event


class ReplayTest(unittest.TestCase):
    def test_same_event_starts_one_workflow(self):
        clients = FakeClients()
        first = lambda_handler(event("evt_replay"), clients=clients)
        second = lambda_handler(event("evt_replay"), clients=clients)
        self.assertEqual(first["statusCode"], 202)
        self.assertEqual(second["statusCode"], 202)
        self.assertEqual(len(clients.stored), 1)
        self.assertEqual(clients.workflows, ["evt_replay"])


if __name__ == "__main__":
    unittest.main()
