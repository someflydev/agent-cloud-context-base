#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${ACCB_TERRAFORM_DIR:-}" ]]; then
  echo "skipped: ACCB_TERRAFORM_DIR not set"
  exit 0
fi

cd "${ACCB_TERRAFORM_DIR}"
terraform init -input=false
terraform workspace select test || terraform workspace new test
terraform plan -input=false -out "${ACCB_TERRAFORM_PLAN:-tfplan}"
terraform apply -input=false -auto-approve "${ACCB_TERRAFORM_PLAN:-tfplan}"
