#!/usr/bin/env bash
set -euo pipefail
EXAMPLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$EXAMPLE/iac/pulumi/dotnet"
pulumi destroy --stack test --yes
