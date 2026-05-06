#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$ROOT/build"
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o "$ROOT/build/bootstrap" ./cmd/lambda
(cd "$ROOT/build" && zip -q function.zip bootstrap)
