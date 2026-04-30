from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


FUNCTION_ARGS = [
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
    "--support-service",
    "aws-s3",
    "--support-service",
    "aws-dynamodb",
    "--support-service",
    "aws-secrets-manager",
]


def run_script(script: str, args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run([PYTHON, "-B", str(ROOT / script), *args], cwd=cwd, text=True, capture_output=True, env=ENV)


def build_generated_repo() -> tempfile.TemporaryDirectory[str]:
    tmp = tempfile.TemporaryDirectory()
    target = Path(tmp.name) / "repo"
    result = run_script("scripts/new_cloud_repo.py", [*FUNCTION_ARGS, "--target-dir", str(target), "--no-init-git"])
    if result.returncode != 0:
        tmp.cleanup()
        raise AssertionError(result.stderr or result.stdout)
    return tmp


def normalize_plan(text: str) -> str:
    lines = text.splitlines()
    if lines:
        lines[0] = "accb new repo plan: <TARGET>"
    return "\n".join(lines) + "\n"
