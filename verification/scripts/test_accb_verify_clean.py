from __future__ import annotations

import unittest
from pathlib import Path

from test_support import build_generated_repo, run_script


class AccbVerifyCleanTest(unittest.TestCase):
    def test_verify_clean_generated_repo(self) -> None:
        tmp = build_generated_repo()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name) / "repo"
        result = run_script("scripts/accb_verify.py", ["--repo", str(repo)])
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("payload mismatches: none", result.stdout)


if __name__ == "__main__":
    unittest.main()
