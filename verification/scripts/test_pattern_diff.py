import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "verification/scripts/fixtures"


class PatternDiffTests(unittest.TestCase):
    def test_matching_fixture_passes(self):
        result = subprocess.run(
            [
                "python3",
                "scripts/pattern_diff.py",
                str(FIXTURES / "pattern_candidate"),
                str(FIXTURES / "pattern_canonical"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_violation_fixture_fails(self):
        result = subprocess.run(
            [
                "python3",
                "scripts/pattern_diff.py",
                str(FIXTURES / "pattern_violation"),
                str(FIXTURES / "pattern_canonical"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
