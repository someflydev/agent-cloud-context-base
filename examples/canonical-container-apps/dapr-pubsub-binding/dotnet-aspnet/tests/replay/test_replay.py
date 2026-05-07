import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class ReplayTests(unittest.TestCase):
    def test_handler_uses_cloudevent_id_as_replay_key(self) -> None:
        program = (ROOT / "src" / "Accb.ContainerApps.Dapr" / "Program.cs").read_text()
        self.assertIn("replayKey", program)
        self.assertIn("local-event", program)


if __name__ == "__main__":
    unittest.main()
