#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${ACCB_TERRAFORM_DIR:-}" ]]; then
  echo "skipped: ACCB_TERRAFORM_DIR not set"
  exit 0
fi

cd "${ACCB_TERRAFORM_DIR}"
terraform destroy -input=false -auto-approve
