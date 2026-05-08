#!/usr/bin/env bash
set -euo pipefail

: "${MINISKY_ENDPOINT_URL:=http://localhost:8686}"
echo "teardown minisky resources at ${MINISKY_ENDPOINT_URL}"
