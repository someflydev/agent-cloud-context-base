import pathlib
import sys
import unittest


example = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(example / "src"))

import main


class ServiceSmokeTest(unittest.TestCase):
    def test_health_and_ready(self):
        self.assertTrue(main.health()["ok"])
        self.assertIn("pubsub", main.ready()["checks"])

    def test_submission_contract(self):
        result = main.submit({"submission_id": "case-123"})
        self.assertEqual(result["submission_id"], "case-123")
        self.assertIn("workflow/case-123", result["state_document"])


if __name__ == "__main__":
    unittest.main()
