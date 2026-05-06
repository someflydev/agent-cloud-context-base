#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_LOCAL_PROVIDER:-0}" != "1" ]]; then
  echo "skipping Lane A miniblue; set ACCB_RUN_LOCAL_PROVIDER=1 to run"
  exit 0
fi
cd "$(dirname "$0")"
docker compose up -d
trap './teardown.sh' EXIT
./bootstrap.sh
python3 test_handler.py
