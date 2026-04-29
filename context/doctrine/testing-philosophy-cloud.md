# Testing Philosophy Cloud

Cloud tests should prove the workload contract at the cheapest layer that still exercises the risk. Unit tests protect logic, smoke tests protect entry points, and integration tests protect managed-service behavior without pretending mocks are cloud infrastructure.

## Use Layered Tests

- Write unit tests for pure logic such as validators, transforms, routing decisions, and idempotency-key builders.
- Keep unit tests free of provider clients, network calls, and cloud credentials.
- Use smoke tests to exercise the deployed entry point shape with mocked managed-service clients.
- Smoke a function handler with representative event payloads.
- Smoke a container through `/healthz`, request handling, and worker startup where applicable.
- Smoke Kubernetes readiness with pod probes, service wiring, and job invocation.

## Separate Smoke From Integration

- Treat smoke tests as fast entry-point confidence.
- Treat integration tests as boundary proof against emulators, real cloud resources, or recorded external calls.
- Do not call a mocked S3, Pub/Sub, Event Grid, or database client an integration test.
- Do not require every smoke test to provision cloud infrastructure.
- Name the intended test lane in the manifest before implementation.

## Choose An Integration Lane

- Use Lane A for local emulator or mock infrastructure such as LocalStack, GCP emulators, and Azurite.
- Use Lane B for ephemeral real cloud resources created through the `test` workspace or stack.
- Prefer Lane B for medium, large, and cross-cloud profiles where provider behavior matters.
- Use Lane C for record/replay when third-party APIs are costly, rate-limited, or contract-stable.
- Keep each lane explicit so operators understand cost, speed, and fidelity.

## Prove Cloud Effects

- Assert persistence at the managed-service boundary, not only return values.
- Verify duplicate event delivery does not duplicate state.
- Verify retry and DLQ behavior for event-driven workloads.
- Verify IAM, service account, or managed identity access through IaC-defined bindings.
- Verify logs and metrics include required correlation fields without exposing secrets.

## Keep CI Operator Driven

- Do not add CI workflows by default in generated repos.
- Provide commands and validation hooks that an operator can wire into CI.
- Make destructive integration tests opt-in unless the manifest declares an ephemeral test lane.
- Destroy Lane B test resources by default after the test run.
- Mark completion `incomplete` when cloud proof is skipped by operator choice.
