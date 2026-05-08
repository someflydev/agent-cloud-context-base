#!/usr/bin/env bash
set -euo pipefail

if [[ "${ACCB_RUN_REAL_CLOUD:-}" != "1" ]]; then
  echo "skipped: ACCB_RUN_REAL_CLOUD=1 not set"
  exit 0
fi

: "${ACCB_MAX_REAL_CLOUD_SECONDS:=900}"
cd "$(dirname "$0")"
python3 runner.py
