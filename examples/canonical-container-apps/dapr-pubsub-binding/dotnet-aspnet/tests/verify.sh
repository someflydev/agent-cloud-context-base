#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/dotnet"
bash "$EXAMPLE/tests/smoke/run.sh"
python3 -m unittest "$EXAMPLE/tests/smoke/test_service.py"
python3 -m unittest "$EXAMPLE/tests/replay/test_replay.py"
