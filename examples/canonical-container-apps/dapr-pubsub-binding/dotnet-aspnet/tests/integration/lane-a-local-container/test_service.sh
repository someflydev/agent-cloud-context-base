#!/usr/bin/env bash
set -euo pipefail
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS http://127.0.0.1:8080/readyz
curl -fsS -X POST http://127.0.0.1:8080/orders -H 'content-type: application/json' -d '{"orderId":"lane-a"}'
