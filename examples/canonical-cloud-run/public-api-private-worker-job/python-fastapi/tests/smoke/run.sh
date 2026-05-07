#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
IMAGE="accb-cloudrun-public-worker:smoke"
NAME="accb-cloudrun-public-worker-smoke"
PORT="${ACCB_SMOKE_PORT:-18080}"
docker build -t "$IMAGE" .
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run --rm -d --name "$NAME" -p "$PORT:8080" "$IMAGE" >/dev/null
cleanup() {
  docker stop "$NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT
for _ in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:$PORT/healthz" >/dev/null; then
    break
  fi
  sleep 1
done
curl -fsS "http://127.0.0.1:$PORT/healthz" >/dev/null
curl -fsS "http://127.0.0.1:$PORT/readyz" >/dev/null
curl -fsS -X POST "http://127.0.0.1:$PORT/submit" -H 'content-type: application/json' -d '{"submission_id":"smoke"}' >/dev/null
