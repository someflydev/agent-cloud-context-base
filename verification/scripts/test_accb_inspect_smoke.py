from __future__ import annotations

import unittest
from pathlib import Path

from test_support import build_generated_repo, run_script


class AccbInspectSmokeTest(unittest.TestCase):
    def test_inspect_prints_profile_tree(self) -> None:
        tmp = build_generated_repo()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name) / "repo"
        result = run_script("scripts/accb_inspect.py", ["--repo", str(repo)])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Profile", result.stdout)
        self.assertIn("validation_gates", result.stdout)
        self.assertIn("aws-lambda-python", result.stdout)


if __name__ == "__main__":
    unittest.main()
