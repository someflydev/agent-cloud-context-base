#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]]; then
  echo "skipping Lane B App Runner probe; set ACCB_RUN_REAL_CLOUD=1 to run"
  exit 0
fi
: "${ACCB_APPRUNNER_TEST_SERVICE_URL:?required}"
curl -fsS "$ACCB_APPRUNNER_TEST_SERVICE_URL/healthz"
curl -fsS "$ACCB_APPRUNNER_TEST_SERVICE_URL/readyz"
curl -fsS -X POST "$ACCB_APPRUNNER_TEST_SERVICE_URL/suppliers/onboard" -H 'content-type: application/json' -d '{"supplier_id":"lane-b"}'
