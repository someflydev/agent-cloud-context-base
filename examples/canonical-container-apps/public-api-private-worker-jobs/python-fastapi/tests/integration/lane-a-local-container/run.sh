#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${ACCB_RUN_LOCAL_PROVIDER:-0}" != "1" ]]; then
  echo "skipping Lane A; set ACCB_RUN_LOCAL_PROVIDER=1 to run docker compose with miniblue"
  exit 0
fi
cd "$DIR"
bash bootstrap.sh
docker compose up --build -d
trap 'bash teardown.sh' EXIT
sleep 3
bash test_service.sh
