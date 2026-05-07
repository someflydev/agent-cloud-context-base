from __future__ import annotations
import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from handler import Clients, handle_firebase_user

class Firestore:
    def __init__(self): self.claimed=set(); self.profiles={}
    def claim_user_event(self, dedupe_key, payload):
        if dedupe_key in self.claimed: return False
        self.claimed.add(dedupe_key); return True
    def write_profile(self, uid, payload): self.profiles[uid]=payload
class PubSub:
    def __init__(self): self.messages=[]
    def publish(self, topic, payload): self.messages.append({"topic":topic,"payload":payload})

class HandlerTest(unittest.TestCase):
    def test_replay_safe_effect(self):
        firestore = Firestore(); pubsub = PubSub()
        clients = Clients(firestore=firestore, pubsub=pubsub)
        event = json.loads('{"id":"evt-1","data":{"uid":"user-1","email":"u@example.com"}}')
        first = handle_firebase_user(event, clients)
        second = handle_firebase_user(event, clients)
        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(firestore.profiles["user-1"]["status"], "ONBOARDING_STARTED")
        self.assertEqual(len(pubsub.messages), 1)
if __name__ == "__main__": unittest.main()
