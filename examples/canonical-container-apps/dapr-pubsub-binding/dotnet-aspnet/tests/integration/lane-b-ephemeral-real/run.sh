#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]]; then
  echo "skipping Lane B; set ACCB_RUN_REAL_CLOUD=1 for isolated Azure test deployment"
  exit 0
fi
bash "$DIR/up.sh"
trap 'bash "$DIR/down.sh"' EXIT
bash "$DIR/test_service.sh"
