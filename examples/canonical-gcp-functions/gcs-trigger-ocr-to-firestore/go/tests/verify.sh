#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/go"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/go"
cd "$EXAMPLE"
go test ./tests/smoke ./tests/replay
