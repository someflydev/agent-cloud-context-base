import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ValidateContextTests(unittest.TestCase):
    def test_current_repo_clean(self):
        result = subprocess.run(
            ["python3", "scripts/validate_context.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_help(self):
        result = subprocess.run(
            ["python3", "scripts/validate_context.py", "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
