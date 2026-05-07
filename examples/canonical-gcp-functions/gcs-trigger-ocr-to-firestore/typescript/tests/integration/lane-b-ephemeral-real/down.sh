#!/usr/bin/env bash
set -euo pipefail
timeout 1800 pulumi destroy --stack test --yes
