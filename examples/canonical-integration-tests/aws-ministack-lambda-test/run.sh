#!/usr/bin/env bash
set -euo pipefail

if [[ "${ACCB_RUN_LOCAL_PROVIDER:-}" != "1" ]]; then
  echo "skipped: ACCB_RUN_LOCAL_PROVIDER=1 not set"
  exit 0
fi

cd "$(dirname "$0")"
./bootstrap.sh
trap './teardown.sh' EXIT
python3 -m pytest tests
