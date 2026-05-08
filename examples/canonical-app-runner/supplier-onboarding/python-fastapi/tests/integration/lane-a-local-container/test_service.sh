#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${ACCB_SERVICE_URL:-http://127.0.0.1:8082}"
curl -fsS "$BASE_URL/healthz"
curl -fsS "$BASE_URL/readyz"
curl -fsS -X POST "$BASE_URL/suppliers/onboard" -H 'content-type: application/json' -d '{"supplier_id":"lane-a"}'
