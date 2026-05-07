#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]]; then
  echo "skipping Lane B Cloud Run probe; set ACCB_RUN_REAL_CLOUD=1 to run"
  exit 0
fi
: "${ACCB_CLOUDRUN_TEST_SERVICE_URL:?required}"
curl -fsS "$ACCB_CLOUDRUN_TEST_SERVICE_URL/healthz"
curl -fsS "$ACCB_CLOUDRUN_TEST_SERVICE_URL/readyz"
curl -fsS -X POST "$ACCB_CLOUDRUN_TEST_SERVICE_URL/trace" -H 'content-type: application/json' -d '{"span_name":"lane-b"}'
