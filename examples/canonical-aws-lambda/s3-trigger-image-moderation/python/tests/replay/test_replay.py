import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "smoke"))

from handler import Clients, lambda_handler
from test_handler import Events, Rekognition, Table, event


class ReplayTest(unittest.TestCase):
    def test_same_object_version_has_one_side_effect(self):
        table = Table()
        events = Events()
        clients = Clients(table, Rekognition(), events)
        first = lambda_handler(event("v1"), clients=clients)
        second = lambda_handler(event("v1"), clients=clients)
        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(len(table.items), 1)
        self.assertEqual(len(events.entries), 1)


if __name__ == "__main__":
    unittest.main()
