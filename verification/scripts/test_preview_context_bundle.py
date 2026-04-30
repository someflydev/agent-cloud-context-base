import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PreviewContextBundleTests(unittest.TestCase):
    def test_feature_gate_notice_passes(self):
        result = subprocess.run(
            ["python3", "scripts/preview_context_bundle.py", "func-aws-lambda-python"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("feature gated off", result.stdout)

    def test_help(self):
        result = subprocess.run(
            ["python3", "scripts/preview_context_bundle.py", "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
