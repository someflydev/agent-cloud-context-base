from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
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

firestore = Firestore(); pubsub = PubSub()
clients = Clients(firestore=firestore, pubsub=pubsub)
result = handle_firebase_user(json.loads('{"id":"evt-1","data":{"uid":"user-1","email":"u@example.com"}}'), clients)
assert result["duplicate"] is False
assert len(pubsub.messages) == 1
