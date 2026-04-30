import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class RunVerificationTests(unittest.TestCase):
    def test_fast_tier_passes(self):
        result = subprocess.run(
            ["python3", "scripts/run_verification.py", "--tier", "fast"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_help(self):
        result = subprocess.run(
            ["python3", "scripts/run_verification.py", "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
