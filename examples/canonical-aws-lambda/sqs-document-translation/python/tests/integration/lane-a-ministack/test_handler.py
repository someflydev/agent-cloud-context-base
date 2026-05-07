import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "smoke"))
from handler import lambda_handler
from test_handler import FakeClients, event
clients = FakeClients()
first = lambda_handler(event("msg_lane_a"), clients=clients)
second = lambda_handler(event("msg_lane_a"), clients=clients)
assert first["processed"] == 1
assert second["duplicates"] == 1
assert len(clients.artifacts) == 1
print("Lane A Python SQS translation passed")
