import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class DaprServiceTests(unittest.TestCase):
    def test_program_exposes_health_ready_and_pubsub_routes(self) -> None:
        program = (ROOT / "src" / "Accb.ContainerApps.Dapr" / "Program.cs").read_text()
        self.assertIn("/healthz", program)
        self.assertIn("/readyz", program)
        self.assertIn("/orders", program)

    def test_dapr_components_are_scoped(self) -> None:
        pubsub = (ROOT / "dapr" / "components" / "pubsub.yaml").read_text()
        self.assertIn("scopes:", pubsub)
        self.assertIn("publisher", pubsub)
        self.assertIn("subscriber", pubsub)


if __name__ == "__main__":
    unittest.main()
