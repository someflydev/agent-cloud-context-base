#!/usr/bin/env bash
set -euo pipefail

: "${MINISTACK_ENDPOINT_URL:=http://localhost:4566}"
: "${ACCB_TEST_PREFIX:=accb-test}"

echo "teardown ministack resources at ${MINISTACK_ENDPOINT_URL}"
aws --endpoint-url "${MINISTACK_ENDPOINT_URL}" s3 rb "s3://${ACCB_TEST_PREFIX}-images-test" --force >/dev/null || true
aws --endpoint-url "${MINISTACK_ENDPOINT_URL}" dynamodb delete-table \
  --table-name "${ACCB_TEST_PREFIX}-decisions-test" >/dev/null || true
aws --endpoint-url "${MINISTACK_ENDPOINT_URL}" sqs delete-queue \
  --queue-url "${MINISTACK_ENDPOINT_URL}/000000000000/${ACCB_TEST_PREFIX}-events-test" >/dev/null || true
