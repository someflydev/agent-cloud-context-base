#!/usr/bin/env bash
set -euo pipefail
EXAMPLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
test -f "$EXAMPLE/src/Accb.ContainerApps.Dapr/Program.cs"
test -f "$EXAMPLE/dapr/components/pubsub.yaml"
test -f "$EXAMPLE/dapr/components/state.yaml"
test -f "$EXAMPLE/dapr/components/secrets.yaml"
grep -q "/healthz" "$EXAMPLE/src/Accb.ContainerApps.Dapr/Program.cs"
grep -q "/readyz" "$EXAMPLE/src/Accb.ContainerApps.Dapr/Program.cs"
grep -q "/orders-handler" "$EXAMPLE/src/Accb.ContainerApps.Dapr/Program.cs"
