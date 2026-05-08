#!/usr/bin/env bash
set -euo pipefail

: "${MINISTACK_ENDPOINT_URL:=http://localhost:4566}"
: "${ACCB_TEST_PREFIX:=accb-test}"

echo "bootstrap ministack resources at ${MINISTACK_ENDPOINT_URL}"
aws --endpoint-url "${MINISTACK_ENDPOINT_URL}" s3 mb "s3://${ACCB_TEST_PREFIX}-images-test" >/dev/null
aws --endpoint-url "${MINISTACK_ENDPOINT_URL}" dynamodb create-table \
  --table-name "${ACCB_TEST_PREFIX}-decisions-test" \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST >/dev/null
aws --endpoint-url "${MINISTACK_ENDPOINT_URL}" sqs create-queue \
  --queue-name "${ACCB_TEST_PREFIX}-events-test" >/dev/null
