#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-azure-functions/servicebus-classification/dotnet-isolated"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/dotnet"
python3 -m unittest "$EXAMPLE/tests/smoke/test_handler.py"
PYTHONPATH="$EXAMPLE" python3 -m unittest "$EXAMPLE/tests/replay/test_replay.py"
