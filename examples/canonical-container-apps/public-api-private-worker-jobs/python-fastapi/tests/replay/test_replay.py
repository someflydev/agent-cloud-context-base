import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[2] / "src" / "main.py"
SPEC = importlib.util.spec_from_file_location("aca_public_worker_replay", MODULE_PATH)
main = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(main)


class ReplayTests(unittest.TestCase):
    def test_process_uses_message_id_as_replay_key_source(self) -> None:
        result = main.process({"message_id": "sb-1"})
        self.assertEqual(result["message_id"], "sb-1")
        self.assertTrue(result["internal_ingress"])


if __name__ == "__main__":
    unittest.main()
