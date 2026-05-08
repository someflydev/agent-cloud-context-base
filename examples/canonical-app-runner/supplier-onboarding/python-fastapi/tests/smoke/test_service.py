import pathlib
import sys
import unittest


example = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(example / "src"))

import main


class ServiceSmokeTest(unittest.TestCase):
    def test_health_and_ready(self):
        self.assertTrue(main.health()["ok"])
        self.assertIn("database_host", main.ready())

    def test_supplier_route_contract(self):
        result = main.onboard_supplier({"supplier_id": "supplier-1"})
        self.assertEqual(result["supplier_id"], "supplier-1")
        self.assertEqual(result["profile_state"], "pending_review")


if __name__ == "__main__":
    unittest.main()
