import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "src"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "smoke"))
from handler import lambda_handler
from test_handler import FakeClients, event
clients = FakeClients()
lambda_handler(event(), clients=clients)
lambda_handler(event(), clients=clients)
assert len(clients.profiles) == 1
assert len(clients.events) == 1
print("Lane A Cognito post-confirmation passed")
