#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/typescript"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/typescript"
node "$EXAMPLE/tests/smoke/test_handler.js"
node "$EXAMPLE/tests/replay/test_replay.js"
