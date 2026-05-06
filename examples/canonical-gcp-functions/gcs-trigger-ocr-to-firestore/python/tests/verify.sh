#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/python"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/python"
python3 -m unittest "$EXAMPLE/tests/smoke/test_handler.py"
python3 -m unittest "$EXAMPLE/tests/replay/test_replay.py"
