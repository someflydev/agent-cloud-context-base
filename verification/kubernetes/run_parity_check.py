#!/usr/bin/env python3
"""Check canonical Kubernetes example parity."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parity_common import run_family_parity


if __name__ == "__main__":
    raise SystemExit(run_family_parity({"canonical-eks", "canonical-gke", "canonical-aks"}))
