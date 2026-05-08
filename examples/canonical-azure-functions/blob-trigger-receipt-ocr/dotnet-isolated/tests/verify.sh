#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-azure-functions/blob-trigger-receipt-ocr/dotnet-isolated"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/dotnet"
python3 -m unittest "$EXAMPLE/tests/smoke/test_handler.py"
PYTHONPATH="$EXAMPLE" python3 -m unittest "$EXAMPLE/tests/replay/test_replay.py"
if command -v dotnet >/dev/null 2>&1; then
  dotnet run --project "$EXAMPLE/tests/smoke/HandlerHarness.csproj"
else
  printf '%s\n' "dotnet not found; skipped optional real .NET handler harness"
fi
