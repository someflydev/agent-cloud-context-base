import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(root))

from examples.canonical_azure_functions_import import load_python_handler

handler = load_python_handler(
    "examples/canonical-azure-functions/eventgrid-alert-router/python/src/handler.py"
)
result = handler.route_alert({"id": "lane-a-alert", "resource_id": "/subscriptions/local/resourceGroups/rg", "severity": "Sev2"})
assert result["service_bus_message"]["message_id"] == result["idempotency_key"]
print("lane-a-miniblue eventgrid alert router passed")
