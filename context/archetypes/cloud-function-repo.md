# Cloud Function Repo

Use this archetype for the narrowest cloud repository: one provider-native function, one trigger boundary, one explicit IaC dev/test pair, and a small set of managed-service bindings. It is the default when the workload is a bounded event, HTTP, storage, queue, or scheduler handler that does not need a custom long-running runtime.

## Common Goals

- Generate one deployable function with a clear handler contract.
- Declare dev and test state, env-var prefix, secret path, and resource naming.
- Bind one trigger to one idempotent handler path.
- Keep persistence and event side effects small enough to prove in test.
- Exercise the real provider trigger fixture or emulator boundary before completion.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/doctrine/trigger-boundary-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/cloud-secret-handling.md`
- the dominant provider+function+language stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-aws-lambda/`, `examples/canonical-gcp-functions/`, or `examples/canonical-azure-functions/`

## Common Workflows

- `context/workflows/add-cloud-function.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-cloud-smoke-tests.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/func-aws-lambda-python.yaml`
- `manifests/func-aws-lambda-typescript.yaml`
- `manifests/func-gcp-cloudfn-python.yaml`
- `manifests/func-azure-fn-python.yaml`

## Likely Examples

- `examples/canonical-aws-lambda/s3-trigger-image-moderation/`
- `examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/`
- `examples/canonical-azure-functions/blob-trigger-receipt-ocr/`

## Typical Anti-Patterns

- Running long polling loops inside the handler.
- Mocking a managed service in the integration test and calling it complete.
- Sharing dev and test state backend keys, secret paths, or resource names.
- Adding a private worker or scheduled job without rerouting the archetype.
- Baking a secret value into source, function config, or test fixtures.

## Validation Gates (summary)

- function-trigger-contract: Exercise the function with a real trigger event fixture.
- function-idempotency-proof: Replay the same trigger with the same dedupe key and assert exactly-once effect.
- iac-dev-test-disjoint: Prove dev and test use separate state, names, env prefixes, and secret paths.
- secret-not-in-source: Confirm source, IaC config, logs, and fixtures contain no secret values.
