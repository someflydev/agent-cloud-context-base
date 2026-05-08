#!/usr/bin/env bash
set -euo pipefail
EXAMPLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROGRAM="$EXAMPLE/src/Accb.ContainerApps.PublicWorker/Program.cs"
grep -q '"/healthz"' "$PROGRAM"
grep -q '"/readyz"' "$PROGRAM"
grep -q '"/submit"' "$PROGRAM"
grep -q '"/process"' "$PROGRAM"
grep -q '"/retry"' "$PROGRAM"
