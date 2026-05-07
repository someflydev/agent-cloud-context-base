from __future__ import annotations
import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from handler import Clients, handle_pubsub_message

class Firestore:
    def __init__(self): self.claimed=set(); self.records={}
    def claim_message(self, dedupe_key, payload):
        if dedupe_key in self.claimed: return False
        self.claimed.add(dedupe_key); return True
    def write_translation(self, dedupe_key, payload): self.records[dedupe_key]=payload
class Translate:
    def translate(self, text, target_locale): return f"{text}:{target_locale}"
class PubSub:
    def __init__(self): self.messages=[]
    def publish(self, topic, payload): self.messages.append({"topic":topic,"payload":payload})

class HandlerTest(unittest.TestCase):
    def test_replay_safe_effect(self):
        firestore = Firestore(); pubsub = PubSub()
        clients = Clients(firestore=firestore, translate=Translate(), pubsub=pubsub)
        event = json.loads('{"id":"evt-1","data":{"messageId":"msg-1","text":"hello","targetLocale":"es"}}')
        first = handle_pubsub_message(event, clients)
        second = handle_pubsub_message(event, clients)
        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(firestore.records["msg-1:es"]["status"], "TRANSLATED")
        self.assertEqual(len(pubsub.messages), 1)
if __name__ == "__main__": unittest.main()
