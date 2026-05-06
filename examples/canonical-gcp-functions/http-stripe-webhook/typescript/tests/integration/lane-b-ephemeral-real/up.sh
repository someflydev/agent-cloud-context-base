#!/usr/bin/env bash
set -euo pipefail
echo "Lane B requires ACCB_RUN_REAL_CLOUD=1, GCP credentials, and an isolated test project."
[[ "${ACCB_RUN_REAL_CLOUD:-0}" == "1" ]]
pulumi up --stack test --yes
