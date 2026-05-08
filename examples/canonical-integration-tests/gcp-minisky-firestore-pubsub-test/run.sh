#!/usr/bin/env bash
set -euo pipefail

if [[ "${ACCB_RUN_LOCAL_PROVIDER:-}" != "1" ]]; then
  echo "skipped: ACCB_RUN_LOCAL_PROVIDER=1 not set"
  exit 0
fi

cd "$(dirname "$0")"
./setup.sh
trap './teardown.sh' EXIT
functions-framework --target handler --port "${ACCB_FUNCTIONS_PORT:-8080}" &
server_pid=$!
trap 'kill ${server_pid} 2>/dev/null || true; ./teardown.sh' EXIT
python3 -m pytest tests
