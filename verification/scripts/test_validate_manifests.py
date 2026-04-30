import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ValidateManifestsTests(unittest.TestCase):
    def test_current_repo_clean(self):
        result = subprocess.run(
            ["python3", "scripts/validate_manifests.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_manifest_fails(self):
        result = subprocess.run(
            ["python3", "scripts/validate_manifests.py", "does-not-exist"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
