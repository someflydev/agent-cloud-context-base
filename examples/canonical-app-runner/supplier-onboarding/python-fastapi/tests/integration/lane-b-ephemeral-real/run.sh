#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]]; then
  echo "skipping Lane B App Runner run; set ACCB_RUN_REAL_CLOUD=1 to run"
  exit 0
fi
cd "$(dirname "$0")"
MAX_SECONDS="${ACCB_REAL_CLOUD_MAX_RUNTIME_SECONDS:-1800}"
(sleep "$MAX_SECONDS"; echo "Lane B max runtime exceeded after ${MAX_SECONDS}s" >&2; kill "$$") &
WATCHDOG=$!
cleanup() {
  ./down.sh || true
  kill "$WATCHDOG" >/dev/null 2>&1 || true
}
trap cleanup EXIT
./up.sh
./test_service.sh
