#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${ACCB_SERVICE_URL:-http://127.0.0.1:8081}"
curl -fsS "$BASE_URL/healthz"
curl -fsS "$BASE_URL/readyz"
curl -fsS -X POST "$BASE_URL/trace" -H 'content-type: application/json' -d '{"span_name":"lane-a"}'
