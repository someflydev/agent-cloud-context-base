# Functions Arc Overview

## Arc Goal

The functions arc proves that accb can generate event-driven and HTTP-triggered serverless repositories across AWS Lambda, GCP Cloud Functions, and Azure Functions without losing the same testing, observability, secret, eventing, and IaC isolation contracts.

## Examples Authored

- aws x python: `canonical-aws-lambda/s3-trigger-image-moderation`
- aws x typescript: `canonical-aws-lambda/s3-trigger-image-moderation`
- aws x go: `canonical-aws-lambda/s3-trigger-image-moderation`
- aws x typescript: `canonical-aws-lambda/apigw-stripe-webhook`
- aws x python: `canonical-aws-lambda/apigw-stripe-webhook`
- aws x go: `canonical-aws-lambda/sqs-document-translation`
- aws x python: `canonical-aws-lambda/sqs-document-translation`
- aws x typescript: `canonical-aws-lambda/eventbridge-cdc-relay`
- aws x python: `canonical-aws-lambda/cognito-post-confirmation`
- gcp x python: `canonical-gcp-functions/gcs-trigger-ocr-to-firestore`
- gcp x typescript: `canonical-gcp-functions/http-stripe-webhook`
- gcp x go: `canonical-gcp-functions/eventarc-monitoring-router`
- gcp x typescript: `canonical-gcp-functions/gcs-trigger-ocr-to-firestore`
- gcp x go: `canonical-gcp-functions/gcs-trigger-ocr-to-firestore`
- gcp x python: `canonical-gcp-functions/pubsub-translation-stream`
- gcp x python: `canonical-gcp-functions/firebase-onboarding`
- azure x python: `canonical-azure-functions/blob-trigger-receipt-ocr`
- azure x dotnet-isolated: `canonical-azure-functions/servicebus-classification`
- azure x typescript: `canonical-azure-functions/cosmos-changefeed-search-sync`
- azure x typescript: `canonical-azure-functions/blob-trigger-receipt-ocr`
- azure x dotnet-isolated: `canonical-azure-functions/blob-trigger-receipt-ocr`
- azure x python: `canonical-azure-functions/eventgrid-alert-router`

## Doctrines Anchored

- `context/doctrine/serverless-state-discipline.md`
- `context/doctrine/trigger-boundary-discipline.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/testing-philosophy-cloud.md`

## Stacks Anchored

- `context/stacks/aws-lambda-python.md`
- `context/stacks/aws-lambda-typescript-node.md`
- `context/stacks/aws-lambda-go.md`
- `context/stacks/gcp-cloudfn-python.md`
- `context/stacks/gcp-cloudfn-typescript-node.md`
- `context/stacks/gcp-cloudfn-go.md`
- `context/stacks/azure-fn-python.md`
- `context/stacks/azure-fn-typescript-node.md`
- `context/stacks/azure-fn-dotnet-isolated.md`

## Workflows Anchored

- `context/workflows/add-aws-lambda-trigger.md`
- `context/workflows/add-cloud-function.md`
- `context/workflows/add-azure-function-trigger.md`

## Scenario Patterns Covered

| Scenario pattern | Canonical example families |
| --- | --- |
| `function.object-intake-enrichment` | `canonical-aws-lambda`, `canonical-azure-functions`, `canonical-gcp-functions` |
| `function.signed-webhook-orchestrator` | `canonical-aws-lambda`, `canonical-azure-functions`, `canonical-gcp-functions` |
| `function.queue-backed-worker` | `canonical-aws-lambda`, `canonical-azure-functions`, `canonical-gcp-functions` |
| `function.change-event-relay` | `canonical-aws-lambda`, `canonical-azure-functions`, `canonical-gcp-functions` |
| `function.identity-or-alert-trigger` | `canonical-aws-lambda`, `canonical-azure-functions`, `canonical-gcp-functions` |
| `function.scheduled-report-or-maintenance` | `canonical-aws-lambda`, `canonical-azure-functions`, `canonical-gcp-functions` |

## Validation Gates

| Gate ID | Covering example |
| --- | --- |
| `functions-gate-01` | smoke verify.sh: `canonical-aws-lambda/s3-trigger-image-moderation/python` |
| `functions-gate-02` | structured-log-shape: `canonical-aws-lambda/s3-trigger-image-moderation/typescript` |
| `functions-gate-03` | terraform dev/test isolation: `canonical-aws-lambda/s3-trigger-image-moderation/go` |
| `functions-gate-04` | pulumi stack isolation: `canonical-aws-lambda/apigw-stripe-webhook/typescript` |
| `functions-gate-05` | replay fixtures: `canonical-aws-lambda/apigw-stripe-webhook/python` |
| `functions-gate-06` | lane-a local provider: `canonical-aws-lambda/sqs-document-translation/go` |
| `functions-gate-07` | lane-b ephemeral real cloud: `canonical-aws-lambda/sqs-document-translation/python` |

## Lane Coverage

| Example | Lane A | Lane B | Lane C |
| --- | --- | --- | --- |
| `canonical-aws-lambda/s3-trigger-image-moderation/python` | yes | yes | deferred |
| `canonical-aws-lambda/s3-trigger-image-moderation/typescript` | yes | yes | deferred |
| `canonical-aws-lambda/s3-trigger-image-moderation/go` | yes | yes | deferred |
| `canonical-aws-lambda/apigw-stripe-webhook/typescript` | yes | yes | deferred |
| `canonical-aws-lambda/apigw-stripe-webhook/python` | yes | yes | deferred |
| `canonical-aws-lambda/sqs-document-translation/go` | yes | yes | deferred |
| `canonical-aws-lambda/sqs-document-translation/python` | yes | yes | deferred |
| `canonical-aws-lambda/eventbridge-cdc-relay/typescript` | yes | yes | deferred |
| `canonical-aws-lambda/cognito-post-confirmation/python` | yes | yes | deferred |
| `canonical-gcp-functions/gcs-trigger-ocr-to-firestore/python` | yes | yes | deferred |
| `canonical-gcp-functions/http-stripe-webhook/typescript` | yes | yes | deferred |
| `canonical-gcp-functions/eventarc-monitoring-router/go` | yes | yes | deferred |
| `canonical-gcp-functions/gcs-trigger-ocr-to-firestore/typescript` | yes | yes | deferred |
| `canonical-gcp-functions/gcs-trigger-ocr-to-firestore/go` | yes | yes | deferred |
| `canonical-gcp-functions/pubsub-translation-stream/python` | yes | yes | deferred |
| `canonical-gcp-functions/firebase-onboarding/python` | yes | yes | deferred |
| `canonical-azure-functions/blob-trigger-receipt-ocr/python` | yes | yes | deferred |
| `canonical-azure-functions/servicebus-classification/dotnet-isolated` | yes | yes | deferred |
| `canonical-azure-functions/cosmos-changefeed-search-sync/typescript` | yes | yes | deferred |
| `canonical-azure-functions/blob-trigger-receipt-ocr/typescript` | yes | yes | deferred |
| `canonical-azure-functions/blob-trigger-receipt-ocr/dotnet-isolated` | yes | yes | deferred |
| `canonical-azure-functions/eventgrid-alert-router/python` | yes | yes | deferred |

## Verification Status

| Example | Smoke | Local provider | Real cloud | Full |
| --- | --- | --- | --- | --- |
| `canonical-aws-lambda/s3-trigger-image-moderation/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/s3-trigger-image-moderation/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/s3-trigger-image-moderation/go` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/apigw-stripe-webhook/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/apigw-stripe-webhook/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/sqs-document-translation/go` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/sqs-document-translation/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/eventbridge-cdc-relay/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-aws-lambda/cognito-post-confirmation/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/gcs-trigger-ocr-to-firestore/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/http-stripe-webhook/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/eventarc-monitoring-router/go` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/gcs-trigger-ocr-to-firestore/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/gcs-trigger-ocr-to-firestore/go` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/pubsub-translation-stream/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-gcp-functions/firebase-onboarding/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-azure-functions/blob-trigger-receipt-ocr/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-azure-functions/servicebus-classification/dotnet-isolated` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-azure-functions/cosmos-changefeed-search-sync/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-azure-functions/blob-trigger-receipt-ocr/typescript` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-azure-functions/blob-trigger-receipt-ocr/dotnet-isolated` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |
| `canonical-azure-functions/eventgrid-alert-router/python` | passed<br>2026-05-08T16:08:04+00:00 | skipped<br>ACCB_RUN_LOCAL_PROVIDER=1 not set | pending | missing |

## Known Gaps + Follow-on Arcs

- Real-cloud Lane B remains operator-gated because it can create billable resources.
- Lane C full release gates are represented only where a canonical release gate exists.
- Deferred scenario patterns in `context/scenarios/scenario-profile-map.yaml` must be promoted by later example-authoring arcs.
- Provider local bundles are harness contracts here; derived repos own provider-specific fixture depth.
- PROMPT_33 wires root README, ARCHITECTURE_MAP, and end-to-end smoke coverage.

## How To Generate A New Repo From This Arc

Select the closest scenario pattern, choose the provider/runtime/language cell from `docs/provider-parity-matrix.md`, then invoke `scripts/new_cloud_repo.py` with the matching manifest. Example:

```bash
python3 scripts/new_cloud_repo.py --archetype cloud-function-repo --provider aws --runtime-tier function --primary-stack aws-lambda-python --primary-language python --iac-tool pulumi-python --manifest func-aws-lambda-python --output ../my-function-repo
```

## Registry Detail

| Family | Provider | Runtime | Language | Terraform | Pulumi | Dev/test disjoint |
| --- | --- | --- | --- | --- | --- | --- |
| `canonical-aws-lambda` | aws | function | python | True | pulumi-python | True |
| `canonical-aws-lambda` | aws | function | typescript | True | pulumi-typescript | True |
| `canonical-aws-lambda` | aws | function | go | True | pulumi-go | True |
| `canonical-aws-lambda` | aws | function | typescript | True | pulumi-typescript | True |
| `canonical-aws-lambda` | aws | function | python | True | pulumi-python | True |
| `canonical-aws-lambda` | aws | function | go | True | pulumi-go | True |
| `canonical-aws-lambda` | aws | function | python | True | pulumi-python | True |
| `canonical-aws-lambda` | aws | function | typescript | True | pulumi-typescript | True |
| `canonical-aws-lambda` | aws | function | python | True | pulumi-python | True |
| `canonical-gcp-functions` | gcp | function | python | True | pulumi-python | True |
| `canonical-gcp-functions` | gcp | function | typescript | True | pulumi-typescript | True |
| `canonical-gcp-functions` | gcp | function | go | True | pulumi-go | True |
| `canonical-gcp-functions` | gcp | function | typescript | True | pulumi-typescript | True |
| `canonical-gcp-functions` | gcp | function | go | True | pulumi-go | True |
| `canonical-gcp-functions` | gcp | function | python | True | pulumi-python | True |
| `canonical-gcp-functions` | gcp | function | python | True | pulumi-python | True |
| `canonical-azure-functions` | azure | function | python | True | pulumi-python | True |
| `canonical-azure-functions` | azure | function | dotnet-isolated | True | pulumi-dotnet | True |
| `canonical-azure-functions` | azure | function | typescript | True | pulumi-typescript | True |
| `canonical-azure-functions` | azure | function | typescript | True | pulumi-typescript | True |
| `canonical-azure-functions` | azure | function | dotnet-isolated | True | pulumi-dotnet | True |
| `canonical-azure-functions` | azure | function | python | True | pulumi-python | True |

## Arc Operating Notes

| Note | Contract impact |
| --- | --- |
| 1 | Catalog and registry must agree before an example is treated as canonical. |
| 2 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 3 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 4 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 5 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 6 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 7 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 8 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 9 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 10 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 11 | Catalog and registry must agree before an example is treated as canonical. |
| 12 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 13 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 14 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
| 15 | Structured logs are part of the runtime contract for examples with executable workloads. |
| 16 | Scenario patterns may point at deferred examples only when the map declares the deferral. |
| 17 | Generated repos should load manifests first and broaden context only when routing requires it. |
| 18 | Registry history is tiered so smoke, local-provider, real-cloud, and full results do not overwrite each other. |
| 19 | Provider-specific runtime behavior is allowed when the example README owns the reason. |
| 20 | PROMPT_33 is responsible for final README, architecture map, and end-to-end generation smoke. |
| 21 | Catalog and registry must agree before an example is treated as canonical. |
| 22 | IaC isolation is validated through the shared script, not per-family bespoke logic. |
| 23 | Lane A local-provider checks remain explicitly gated by environment variables. |
| 24 | Lane B real-cloud checks remain explicitly gated because they can create billable resources. |
