#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-aws-lambda/s3-trigger-image-moderation/go"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/go"
cd "$EXAMPLE"
export GOCACHE="${GOCACHE:-/tmp/accb-go-cache}"
mkdir -p "$GOCACHE"
go test ./tests/smoke ./tests/replay
