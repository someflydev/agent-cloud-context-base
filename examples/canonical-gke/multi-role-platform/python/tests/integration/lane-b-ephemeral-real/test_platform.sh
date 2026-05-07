#!/usr/bin/env bash
set -euo pipefail
if [ "${ACCB_RUN_REAL_CLOUD:-0}" != "1" ]; then
  echo "skipping real cloud platform test"
  exit 0
fi
kubectl wait --for=condition=available deployment --all --all-namespaces --timeout=180s
