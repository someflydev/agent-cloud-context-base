#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_LOCAL_PROVIDER:-0}" != "1" ]]; then
  echo "skipping Lane A ministack; set ACCB_RUN_LOCAL_PROVIDER=1 to run"
  exit 0
fi
cd "$(dirname "$0")/../../.."
docker compose -f tests/integration/lane-a-ministack/docker-compose.yml up -d
trap 'docker compose -f tests/integration/lane-a-ministack/docker-compose.yml down -v' EXIT
tests/integration/lane-a-ministack/bootstrap.sh
go test ./tests/smoke ./tests/replay
