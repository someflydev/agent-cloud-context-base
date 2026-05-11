#!/usr/bin/env bash
set -euo pipefail

if [[ "${ACCB_RUN_LOCAL_PROVIDER:-}" != "1" ]]; then
  echo "skipped: ACCB_RUN_LOCAL_PROVIDER=1 not set"
  exit 0
fi

cd "$(dirname "$0")"
echo "skipped: MiniBlue emulator automation is not available in this repo; provide a concrete Azure Functions test harness before enabling this lane"
exit 0
./setup.sh
trap './teardown.sh' EXIT
dotnet test tests/Miniblue.FunctionTests.csproj
