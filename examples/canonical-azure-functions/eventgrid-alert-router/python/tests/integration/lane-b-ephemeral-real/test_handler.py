from examples.canonical_azure_functions_import import load_python_handler

handler = load_python_handler(
    "examples/canonical-azure-functions/eventgrid-alert-router/python/src/handler.py"
)
result = handler.route_alert({"id": "lane-b-alert", "resource_id": "/subscriptions/test/resourceGroups/rg", "severity": "Sev1"})
assert result["service_bus_message"]["topic"] == "alerts-platform"
print("lane-b Azure Event Grid alert router probe passed")
