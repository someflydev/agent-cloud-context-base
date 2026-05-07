import pathlib
import sys
import unittest


example = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(example / "src"))

import main


class ServiceSmokeTest(unittest.TestCase):
    def test_health_and_ready(self):
        self.assertTrue(main.health()["ok"])
        self.assertIn("127.0.0.1", main.ready()["otel_collector"])

    def test_trace_contract(self):
        self.assertEqual(main.trace({"span_name": "smoke"})["span_name"], "smoke")


if __name__ == "__main__":
    unittest.main()
