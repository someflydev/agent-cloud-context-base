from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
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

firestore = Firestore(); pubsub = PubSub()
clients = Clients(firestore=firestore, translate=Translate(), pubsub=pubsub)
result = handle_pubsub_message(json.loads('{"id":"evt-1","data":{"messageId":"msg-1","text":"hello","targetLocale":"es"}}'), clients)
assert result["duplicate"] is False
assert len(pubsub.messages) == 1
