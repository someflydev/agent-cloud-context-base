#!/usr/bin/env bash
set -euo pipefail

: "${MINIBLUE_ENDPOINT_URL:=http://localhost:7071}"
echo "teardown miniblue resources at ${MINIBLUE_ENDPOINT_URL}"
