#!/usr/bin/env bash
set -euo pipefail
kind delete cluster --name "${ACCB_KIND_CLUSTER:-accb-canonical-gke}"
