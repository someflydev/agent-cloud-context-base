#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../../iac/pulumi/python"
timeout 1800 pulumi up --stack test --yes
