import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class VerifyExamplesTests(unittest.TestCase):
    def test_empty_registry_passes(self):
        result = subprocess.run(
            ["python3", "scripts/verify_examples.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_help(self):
        result = subprocess.run(
            ["python3", "scripts/verify_examples.py", "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
