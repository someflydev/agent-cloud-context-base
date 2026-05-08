#!/usr/bin/env bash
set -euo pipefail
if [ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]; then
  echo "skipping real cloud lane; set ACCB_RUN_REAL_CLOUD=1"
  exit 0
fi
echo "create isolated test cluster with Terraform or Pulumi, then apply k8s overlays/test"
