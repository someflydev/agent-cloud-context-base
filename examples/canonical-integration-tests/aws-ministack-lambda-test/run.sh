#!/usr/bin/env bash
set -euo pipefail

if [[ "${ACCB_RUN_LOCAL_PROVIDER:-}" != "1" ]]; then
  echo "skipped: ACCB_RUN_LOCAL_PROVIDER=1 not set"
  exit 0
fi

cd "$(dirname "$0")"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
./bootstrap.sh
trap './teardown.sh' EXIT
python3 -m pytest tests
