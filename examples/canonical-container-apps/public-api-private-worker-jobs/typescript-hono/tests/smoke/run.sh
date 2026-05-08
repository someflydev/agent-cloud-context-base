#!/usr/bin/env bash
set -euo pipefail
EXAMPLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICE="$EXAMPLE/src/index.ts"
grep -q '"/healthz"' "$SERVICE"
grep -q '"/readyz"' "$SERVICE"
grep -q '"/submit"' "$SERVICE"
grep -q '"/process"' "$SERVICE"
grep -q '"/retry"' "$SERVICE"
