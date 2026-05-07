#!/usr/bin/env bash
set -euo pipefail
EXAMPLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$EXAMPLE/iac/pulumi/python"
pulumi stack select test || pulumi stack init test
pulumi up --stack test --yes
