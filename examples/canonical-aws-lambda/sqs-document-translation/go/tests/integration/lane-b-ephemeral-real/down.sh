#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../../iac/pulumi/go"
timeout 1800 pulumi destroy --stack test --yes
