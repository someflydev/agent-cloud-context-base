#!/usr/bin/env bash
set -euo pipefail
EXAMPLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHONPATH="$EXAMPLE/src" python3 - <<'PY'
import main

assert main.health()["ok"] is True
assert main.ready()["ready"] is True
assert main.submit({"submission_id": "smoke"})["submission_id"] == "smoke"
assert main.process({"message_id": "smoke-message"})["accepted"] is True
PY
