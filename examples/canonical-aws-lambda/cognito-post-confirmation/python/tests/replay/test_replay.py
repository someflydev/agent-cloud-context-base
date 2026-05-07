import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "smoke"))

from handler import lambda_handler
from test_handler import FakeClients, event


class ReplayTest(unittest.TestCase):
    def test_same_confirmation_has_one_side_effect(self):
        clients = FakeClients()
        lambda_handler(event(), clients=clients)
        lambda_handler(event(), clients=clients)
        self.assertEqual(len(clients.profiles), 1)
        self.assertEqual(len(clients.events), 1)


if __name__ == "__main__":
    unittest.main()
