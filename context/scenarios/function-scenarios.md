# Function Scenarios

Function scenarios cover workloads where one trigger boundary can do bounded work, persist state, and optionally publish a downstream event. Escalate to managed containers only when custom binaries, duration, memory, or cold-start behavior break the function fit.

## object-intake-enrichment

- Typical providers: AWS Lambda with S3 and EventBridge; GCP Cloud Functions with GCS and Pub/Sub or Eventarc; Azure Functions with Blob Storage and Event Grid.
- Likely archetype: `cloud-event-pipeline`.
- Likely manifests: `func-aws-lambda-python`, `func-gcp-cloudfn-python`, `func-azure-fn-python`.
- Support-service capabilities: object storage, metadata database, event bus, secret store, optional AI/OCR/moderation service.
- Canonical example families: `examples/canonical-aws-lambda/`, `examples/canonical-gcp-functions/`, `examples/canonical-azure-functions/`.
- Validation gates: `function-trigger-contract`, `function-idempotency-proof`, `storage-real-roundtrip-in-test-stack`, `eventing-dlq-path`.

## signed-webhook-orchestrator

- Typical providers: API Gateway plus Lambda; Cloud Functions or Cloud Run Functions with HTTPS; Azure Functions HTTP trigger.
- Likely archetype: `cloud-function-repo` for one webhook or `multi-function-platform` when multiple vendors share an event seam.
- Likely manifests: `func-aws-lambda-typescript`, `func-gcp-cloudfn-typescript`, `func-azure-fn-dotnet-isolated`.
- Support-service capabilities: secret store for signing keys, durable raw-event storage, idempotency table, queue or topic for async handoff.
- Canonical example families: webhook intake examples under each function provider family.
- Validation gates: `function-trigger-contract`, `function-idempotency-proof`, `secret-binding-via-identity`, `eventing-dlq-path`.

## queue-backed-worker

- Typical providers: Lambda with SQS; Cloud Functions with Pub/Sub; Azure Functions with Service Bus or Storage Queue.
- Likely archetype: `cloud-function-repo` for one worker or `multi-function-platform` when several worker functions share contracts.
- Likely manifests: `func-aws-lambda-python`, `func-gcp-cloudfn-go`, `func-azure-fn-typescript`.
- Support-service capabilities: queue, DLQ, managed storage, secret store, optional notification topic.
- Canonical example families: queue worker examples in AWS, GCP, and Azure function families.
- Validation gates: `function-trigger-contract`, `function-idempotency-proof`, `eventing-dlq-path`, `identity-least-privilege-declared`.

## change-event-relay

- Typical providers: DynamoDB Streams, EventBridge, Kinesis, Pub/Sub, Eventarc, Cosmos change feed, Event Hubs.
- Likely archetype: `cloud-event-pipeline`.
- Likely manifests: `func-aws-lambda-go`, `func-gcp-cloudfn-python`, `func-azure-fn-dotnet-isolated`, `multi-provider-event-pipeline`.
- Support-service capabilities: source stream or change feed, canonical event store, event bus or topic, idempotency marker storage.
- Canonical example families: stream relay and fan-out examples in function provider families.
- Validation gates: `function-trigger-contract`, `function-idempotency-proof`, `eventing-dlq-path`, `storage-real-roundtrip-in-test-stack`.

## identity-or-alert-trigger

- Typical providers: Cognito or EventBridge rules with Lambda; GCP Identity Platform or Cloud Monitoring with Cloud Functions; Entra ID or Monitor with Azure Functions.
- Likely archetype: `cloud-function-repo`.
- Likely manifests: `func-aws-lambda-typescript`, `func-gcp-cloudfn-typescript`, `func-azure-fn-dotnet-isolated`.
- Support-service capabilities: identity provider or monitoring event source, audit database, notification service, secret store.
- Canonical example families: identity hook and alert handler examples under function provider families.
- Validation gates: `function-trigger-contract`, `identity-least-privilege-declared`, `secret-binding-via-identity`, `storage-real-roundtrip-in-test-stack`.

## scheduled-report-or-maintenance

- Typical providers: EventBridge Scheduler with Lambda; Cloud Scheduler with Cloud Functions; Azure Timer Trigger.
- Likely archetype: `cloud-function-repo` for one schedule or `multi-function-platform` for report, cleanup, and notification functions.
- Likely manifests: `func-aws-lambda-python`, `func-gcp-cloudfn-python`, `func-azure-fn-python`.
- Support-service capabilities: scheduler, database or object storage, notification topic, secret store.
- Canonical example families: scheduled maintenance and report examples in function provider families.
- Validation gates: `function-trigger-contract`, `function-idempotency-proof`, `storage-real-roundtrip-in-test-stack`, `iac-dev-test-disjoint`.
