from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "smoke"))

from handler import Clients, handle_gcs_object
from test_handler import Firestore, PubSub, Vision


class ReplayTest(unittest.TestCase):
    def test_same_generation_has_one_effect(self) -> None:
        firestore = Firestore()
        pubsub = PubSub()
        clients = Clients(firestore=firestore, vision=Vision(), pubsub=pubsub)
        event = {"id": "evt-1", "data": {"bucket": "docs", "name": "scan.png", "generation": "7"}}

        first = handle_gcs_object(event, clients)
        second = handle_gcs_object(event, clients)

        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(len(firestore.metadata), 1)
        self.assertEqual(len(pubsub.messages), 1)


if __name__ == "__main__":
    unittest.main()
