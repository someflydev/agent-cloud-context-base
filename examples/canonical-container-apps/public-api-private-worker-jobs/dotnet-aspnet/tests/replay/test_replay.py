import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class ReplayTests(unittest.TestCase):
    def test_process_route_uses_message_id_as_replay_key_source(self) -> None:
        program = (ROOT / "src" / "Accb.ContainerApps.PublicWorker" / "Program.cs").read_text()
        self.assertIn("message_id", program)
        self.assertIn("internal_ingress", program)


if __name__ == "__main__":
    unittest.main()
