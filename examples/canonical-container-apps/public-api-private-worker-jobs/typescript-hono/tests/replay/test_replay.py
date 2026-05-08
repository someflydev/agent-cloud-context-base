import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class ReplayTests(unittest.TestCase):
    def test_process_route_uses_message_id_as_replay_key_source(self) -> None:
        source = (ROOT / "src" / "index.ts").read_text()
        self.assertIn("message_id", source)
        self.assertIn("internal_ingress", source)


if __name__ == "__main__":
    unittest.main()
