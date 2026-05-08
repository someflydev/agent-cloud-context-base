#!/usr/bin/env bash
set -euo pipefail
if [ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]; then
  echo "skipping real cloud teardown"
  exit 0
fi
echo "destroy isolated test cluster; teardown is mandatory"
