from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from handler import Clients, handle_gcs_object


class Firestore:
    def __init__(self) -> None:
        self.claimed: set[str] = set()
        self.metadata: dict[str, dict] = {}

    def claim_generation(self, dedupe_key: str, payload: dict) -> bool:
        if dedupe_key in self.claimed:
            return False
        self.claimed.add(dedupe_key)
        return True

    def write_metadata(self, dedupe_key: str, payload: dict) -> None:
        self.metadata[dedupe_key] = payload


class Vision:
    def ocr(self, bucket: str, name: str, generation: str) -> str:
        return f"ocr:{bucket}/{name}@{generation}"


class PubSub:
    def __init__(self) -> None:
        self.messages: list[dict] = []

    def publish(self, topic: str, payload: dict) -> None:
        self.messages.append({"topic": topic, "payload": payload})


class HandlerSmokeTest(unittest.TestCase):
    def test_ocr_writes_firestore_and_publishes(self) -> None:
        firestore = Firestore()
        pubsub = PubSub()
        clients = Clients(firestore=firestore, vision=Vision(), pubsub=pubsub)
        event = {"id": "evt-1", "data": {"bucket": "docs", "name": "scan.png", "generation": "7"}}

        result = handle_gcs_object(event, clients)

        self.assertFalse(result["duplicate"])
        self.assertEqual(firestore.metadata["docs:scan.png:7"]["status"], "OCR_COMPLETE")
        self.assertEqual(len(pubsub.messages), 1)


if __name__ == "__main__":
    unittest.main()
