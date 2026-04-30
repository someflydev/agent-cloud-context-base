import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "verification/scripts/fixtures"


class ValidateIacIsolationTests(unittest.TestCase):
    def test_clean_fixture_passes(self):
        result = subprocess.run(
            ["python3", "scripts/validate_iac_isolation.py", str(FIXTURES / "iac_clean")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_violation_fixture_fails(self):
        result = subprocess.run(
            ["python3", "scripts/validate_iac_isolation.py", str(FIXTURES / "iac_violation")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
