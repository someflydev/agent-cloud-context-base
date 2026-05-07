#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

for _ in {1..30}; do
  if docker compose exec -T ministack python -c 'import urllib.request; urllib.request.urlopen("http://localhost:4566/_ministack/health")' >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

ms_aws() {
  docker compose exec -T ministack awslocal "$@"
}

ms_aws dynamodb create-table --table-name accb-dev-cdc-changes --attribute-definitions AttributeName=pk,AttributeType=S --key-schema AttributeName=pk,KeyType=HASH --billing-mode PAY_PER_REQUEST
ms_aws events create-event-bus --name accb-dev-cdc-source
ms_aws events create-event-bus --name accb-dev-cdc-relay
