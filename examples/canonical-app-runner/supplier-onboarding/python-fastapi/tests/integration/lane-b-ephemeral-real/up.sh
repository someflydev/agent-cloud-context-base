#!/usr/bin/env bash
set -euo pipefail
if [[ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]]; then
  echo "skipping Lane B App Runner deploy; set ACCB_RUN_REAL_CLOUD=1 to run"
  exit 0
fi
cd "$(dirname "$0")/../../../iac/pulumi/python"
pulumi up --stack test --yes
