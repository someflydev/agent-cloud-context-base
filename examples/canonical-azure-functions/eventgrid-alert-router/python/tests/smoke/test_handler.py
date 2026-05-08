import unittest

from examples.canonical_azure_functions_import import load_python_handler


handler = load_python_handler(
    "examples/canonical-azure-functions/eventgrid-alert-router/python/src/handler.py"
)


class HandlerSmokeTest(unittest.TestCase):
    def test_event_grid_alert_routes_to_team_topic(self):
        result = handler.route_alert(
            {
                "id": "alert-1",
                "subject": "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Web/sites/api",
                "severity": "Sev1",
                "resource_id": "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Web/sites/api",
                "eventType": "Microsoft.Insights.AlertActivated",
            }
        )
        self.assertEqual(result["cosmos_document"]["team"], "platform")
        self.assertEqual(result["service_bus_message"]["topic"], "alerts-platform")


if __name__ == "__main__":
    unittest.main()
