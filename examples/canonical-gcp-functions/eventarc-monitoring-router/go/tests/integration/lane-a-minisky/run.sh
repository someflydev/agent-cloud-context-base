#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_LOCAL_PROVIDER:-0}" != "1" ]]; then
  echo "skipped: set ACCB_RUN_LOCAL_PROVIDER=1 to run Lane A minisky"
  exit 0
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../../.." && pwd)"
cd "$ROOT/examples/canonical-gcp-functions/eventarc-monitoring-router/go/tests/integration/lane-a-minisky"
export FIRESTORE_EMULATOR_HOST="${FIRESTORE_EMULATOR_HOST:-localhost:8085}"
export PUBSUB_EMULATOR_HOST="${PUBSUB_EMULATOR_HOST:-localhost:8086}"
docker compose up -d
trap './teardown.sh' EXIT
bash bootstrap.sh
go run test_handler.go
