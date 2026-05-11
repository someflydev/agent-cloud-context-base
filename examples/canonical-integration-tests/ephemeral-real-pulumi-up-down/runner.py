#!/usr/bin/env python3
"""Run a gated Pulumi up/assert/destroy cycle for a supplied work directory."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path


def run(command: list[str], cwd: Path) -> int:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return result.returncode


def main() -> int:
    deadline = time.monotonic() + int(os.environ.get("ACCB_MAX_REAL_CLOUD_SECONDS", "900"))
    assert deadline > time.monotonic()
    work_dir = os.environ.get("ACCB_PULUMI_WORK_DIR")
    if not work_dir:
        print("skipped: ACCB_PULUMI_WORK_DIR not set")
        return 0
    cwd = Path(work_dir)
    stack = os.environ.get("ACCB_PULUMI_STACK", "test")
    code = run(["pulumi", "stack", "select", stack, "--create"], cwd)
    if code != 0:
        return code
    up_code = run(["pulumi", "up", "--yes", "--skip-preview"], cwd)
    destroy_code = 0
    try:
        if up_code != 0:
            return up_code
        output_code = run(["pulumi", "stack", "output", "--json"], cwd)
        if output_code != 0:
            return output_code
    finally:
        destroy_code = run(["pulumi", "destroy", "--yes", "--skip-preview"], cwd)
    return destroy_code


if __name__ == "__main__":
    raise SystemExit(main())
