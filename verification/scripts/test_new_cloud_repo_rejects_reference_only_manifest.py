from __future__ import annotations

import unittest

from test_support import run_script


class NewCloudRepoRejectsReferenceOnlyManifestTest(unittest.TestCase):
    def test_rejects_iac_only_and_multi_provider_reference_manifests(self) -> None:
        cases = [
            [
                "--archetype",
                "cloud-iac-only-repo",
                "--provider",
                "aws",
                "--runtime-tier",
                "function",
                "--primary-stack",
                "iac-terraform-aws",
                "--primary-language",
                "hcl",
                "--iac-tool",
                "terraform",
                "--manifest",
                "iac-terraform-aws",
            ],
            [
                "--archetype",
                "cloud-multi-provider-experiment",
                "--provider",
                "aws",
                "--runtime-tier",
                "function",
                "--primary-stack",
                "none",
                "--primary-language",
                "python",
                "--iac-tool",
                "terraform",
                "--manifest",
                "multi-provider-event-pipeline",
            ],
        ]
        for args in cases:
            with self.subTest(manifest=args[-1]):
                result = run_script("scripts/new_cloud_repo.py", ["--dry-run", *args, "--target-dir", "/tmp/accb-ref"])
                self.assertEqual(result.returncode, 1)
                self.assertIn("reference-only manifest", result.stderr)
                self.assertIn("PROMPT_24", result.stderr)


if __name__ == "__main__":
    unittest.main()
