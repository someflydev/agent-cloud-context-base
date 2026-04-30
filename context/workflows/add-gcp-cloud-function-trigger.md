# Add GCP Cloud Function Trigger

Use this workflow when adding a Cloud Functions Gen2 workload with an HTTP, GCS, Pub/Sub, Eventarc, Firestore, or Firebase Auth trigger.

## Preconditions

- GCP is the selected provider and Cloud Functions Gen2 is the runtime tier.
- Trigger type, CloudEvent or HTTP fixture, runtime language, and IaC tool are chosen.
- Dev/test projects or resource names, state, env-var prefixes, secret paths, and service accounts are disjoint.

## Sequence

1. Identify the trigger payload shape and whether the function receives HTTP or CloudEvent input.
2. Author the handler with functions-framework decorators or the language equivalent.
3. Declare the function, service account, trigger, event filters, secret references, and required APIs in IaC.
4. Scope IAM permissions to only the trigger source, target services, dedupe store, and DLQ or dead-letter topic.
5. Declare the idempotency key from event id, object generation, Pub/Sub message id, document path, or business key.
6. Add unit tests for payload parsing and pure logic.
7. Add smoke tests that run the functions-framework entry point with representative input.
8. Add Lane A emulator or Lane B ephemeral real integration tests for trigger, effect, retry, and failure routing.
9. Run `terraform plan` or `pulumi preview` for dev and test before marking completion.

## Outputs

- Cloud Functions Gen2 handler, trigger fixture, IaC resources, service account, failure route, and tests.

## Validation Gates

- `cloudfn-trigger-contract` from `profile-rules.json`
- `function-idempotency-proof`
- `eventing-dlq-path`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/trigger-boundary-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/stacks/gcp-cloudfn-python.md`
- `examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/`

## Common Pitfalls

- Treating Eventarc filters as documentation instead of IaC-owned routing.
- Using broad project-level service account permissions.
- Skipping object generation or event id in the dedupe key.
