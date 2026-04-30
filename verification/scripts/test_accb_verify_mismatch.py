from __future__ import annotations

import unittest
from pathlib import Path

from test_support import build_generated_repo, run_script


class AccbVerifyMismatchTest(unittest.TestCase):
    def test_verify_detects_payload_mutation(self) -> None:
        tmp = build_generated_repo()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name) / "repo"
        boot = repo / ".accb/SESSION_BOOT.md"
        boot.write_text(boot.read_text() + "\nmanual drift\n", encoding="utf-8")
        result = run_script("scripts/accb_verify.py", ["--repo", str(repo)])
        self.assertEqual(result.returncode, 1)
        self.assertIn("payload mismatches", result.stdout)


if __name__ == "__main__":
    unittest.main()
