#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
EXAMPLE="$ROOT/examples/canonical-cloud-run/cloudrun-job-nightly-report/python-fastapi"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/terraform"
python3 "$ROOT/scripts/validate_iac_isolation.py" "$EXAMPLE/iac/pulumi/python"
bash "$EXAMPLE/tests/smoke/run.sh"
python3 -m unittest "$EXAMPLE/tests/smoke/test_service.py"
python3 -m unittest "$EXAMPLE/tests/replay/test_replay.py"
