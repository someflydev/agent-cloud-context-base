from __future__ import annotations

import unittest
from pathlib import Path

from test_support import ROOT, normalize_plan, run_script


PROFILES = {
    "function_aws_lambda_python.txt": [
        "--archetype",
        "cloud-function-repo",
        "--provider",
        "aws",
        "--runtime-tier",
        "function",
        "--primary-stack",
        "aws-lambda-python",
        "--primary-language",
        "python",
        "--iac-tool",
        "pulumi-python",
        "--manifest",
        "func-aws-lambda-python",
        "--target-dir",
        "/tmp/accb-function-smoke",
    ],
    "container_cloudrun_fastapi.txt": [
        "--archetype",
        "managed-container-service",
        "--provider",
        "gcp",
        "--runtime-tier",
        "managed_container",
        "--primary-stack",
        "cloudrun-python-fastapi",
        "--primary-language",
        "python",
        "--iac-tool",
        "pulumi-python",
        "--manifest",
        "container-cloudrun-fastapi",
        "--target-dir",
        "/tmp/accb-container-smoke",
    ],
    "k8s_eks_python.txt": [
        "--archetype",
        "k8s-platform-repo",
        "--provider",
        "aws",
        "--runtime-tier",
        "k8s",
        "--primary-stack",
        "eks-base",
        "--primary-language",
        "python",
        "--iac-tool",
        "terraform",
        "--manifest",
        "k8s-eks-multi-role-python",
        "--target-dir",
        "/tmp/accb-k8s-smoke",
    ],
}


class NewCloudRepoDryRunTest(unittest.TestCase):
    def test_dry_run_profiles_match_golden_snapshots(self) -> None:
        golden_dir = ROOT / "verification/scripts/golden"
        for snapshot, args in PROFILES.items():
            with self.subTest(snapshot=snapshot):
                result = run_script("scripts/new_cloud_repo.py", ["--dry-run", *args])
                self.assertEqual(result.returncode, 0, result.stderr)
                expected = (golden_dir / snapshot).read_text(encoding="utf-8")
                self.assertEqual(normalize_plan(result.stdout), expected)


if __name__ == "__main__":
    unittest.main()
