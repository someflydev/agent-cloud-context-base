#!/usr/bin/env python3
"""Check canonical managed-container example parity."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parity_common import run_family_parity


if __name__ == "__main__":
    raise SystemExit(
        run_family_parity({"canonical-cloud-run", "canonical-app-runner", "canonical-container-apps"})
    )
