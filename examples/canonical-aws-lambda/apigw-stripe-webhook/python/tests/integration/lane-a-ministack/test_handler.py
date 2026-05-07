import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "smoke"))
from handler import lambda_handler
from test_handler import FakeClients, event
clients = FakeClients()
result = lambda_handler(event("evt_lane_a"), clients=clients)
assert result["statusCode"] == 202
assert clients.workflows == ["evt_lane_a"]
print("Lane A Python Stripe webhook passed")
