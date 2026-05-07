#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_LOCAL_PROVIDER:-0}" != "1" ]]; then
  echo "skipping Lane A local container; set ACCB_RUN_LOCAL_PROVIDER=1 to run"
  exit 0
fi
cd "$(dirname "$0")"
docker compose --profile provider up -d --build
trap './teardown.sh' EXIT
./test_service.sh
