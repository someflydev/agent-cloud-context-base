from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from test_support import FUNCTION_ARGS, run_script


class AccbPayloadMinimalTest(unittest.TestCase):
    def test_build_payload_minimal_function_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_script(
                "scripts/accb_payload.py",
                [
                    "--archetype",
                    "cloud-function-repo",
                    "--primary-stack",
                    "aws-lambda-python",
                    "--primary-language",
                    "python",
                    "--provider",
                    "aws",
                    "--runtime-tier",
                    "function",
                    "--iac-tool",
                    "pulumi-python",
                    "--manifest",
                    "func-aws-lambda-python",
                    "--support-service",
                    "aws-s3",
                    "--output-dir",
                    tmp,
                ],
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            root = Path(tmp) / ".accb"
            for rel in [
                "profile/selection.json",
                "profile/scenario-patterns.json",
                "specs/PRODUCT.md",
                "validation/CHECKLIST.md",
                "validation/MATRIX.json",
                "validation/COVERAGE.json",
                "SESSION_BOOT.md",
                "INDEX.json",
                "scripts/accb_payload.py",
                "scripts/accb_inspect.py",
                "scripts/accb_verify.py",
            ]:
                self.assertTrue((root / rel).exists(), rel)
            selection = json.loads((root / "profile/selection.json").read_text())
            coverage = json.loads((root / "validation/COVERAGE.json").read_text())
            self.assertEqual(selection["manifest"], "func-aws-lambda-python")
            self.assertIn("function", selection["capabilities"])
            self.assertTrue(selection["validation_gates"])
            self.assertEqual(coverage["summary"]["missing_capabilities"], [])


if __name__ == "__main__":
    unittest.main()
