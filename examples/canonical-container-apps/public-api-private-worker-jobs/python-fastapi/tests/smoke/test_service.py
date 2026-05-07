import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[2] / "src" / "main.py"
SPEC = importlib.util.spec_from_file_location("aca_public_worker", MODULE_PATH)
main = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(main)


class ServiceTests(unittest.TestCase):
    def test_submit_describes_azure_boundaries(self) -> None:
        result = main.submit({"submission_id": "abc"})
        self.assertEqual(result["state_container"], "workflow")
        self.assertIn("servicebus", result["scale_signal"])

    def test_ready_lists_managed_dependencies(self) -> None:
        checks = main.ready()["checks"]
        self.assertIn("key-vault", checks)
        self.assertIn("managed-identity", checks)


if __name__ == "__main__":
    unittest.main()
