import unittest

from examples.canonical_azure_functions_import import load_python_handler


handler = load_python_handler(
    "examples/canonical-azure-functions/eventgrid-alert-router/python/src/handler.py"
)


class ReplayTest(unittest.TestCase):
    def test_event_id_and_resource_are_idempotent(self):
        event = {"id": "alert-replay", "resource_id": "/subscriptions/test/resourceGroups/rg/providers/Microsoft.Sql/servers/db"}
        self.assertEqual(
            handler.route_alert(event)["idempotency_key"],
            handler.route_alert(event)["idempotency_key"],
        )


if __name__ == "__main__":
    unittest.main()
