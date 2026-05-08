#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]]; then
  echo "skipping Lane B Cloud Run deploy; set ACCB_RUN_REAL_CLOUD=1 to run"
  exit 0
fi
cd "$(dirname "$0")/../../../iac/pulumi/go"
pulumi up --stack test --yes
