# Local Cloud Test Providers

Canonical examples use a testing provider interface so cloud-like integration
tests are consistent across AWS, GCP, and Azure without pretending local
providers replace real cloud verification.

## Test Levels

1. Unit / smoke tests run with mocked SDK clients and no cloud service.
2. Local provider integration runs against a provider-shaped local service:
   `ministack` for AWS, `minisky` for GCP, and `miniblue` for Azure.
3. Ephemeral real cloud tests deploy isolated test infrastructure with real
   credentials, run the proof, and immediately destroy the resources.
4. Optional full / release gates run broader real-cloud coverage for release
   confidence.

## Lane Names

- Lane A is local provider integration.
- Lane B is ephemeral real cloud.
- Lane C is record/replay for third-party APIs or managed AI calls that need
  deterministic replay beyond provider emulation.

## Provider Mapping

- AWS examples use `ministack` (`ministackorg/ministack:latest`) for
  Lambda-adjacent services such as S3, DynamoDB, SQS, SNS, EventBridge,
  Step Functions, Secrets Manager, IAM, and logs.
- GCP examples use `minisky` from `qamarudeenm/minisky`; until a public
  registry image is verified, compose harnesses build from the public GitHub
  repository or use the installed `minisky` binary.
- Azure examples use `miniblue` (`moabukar/miniblue:latest`) for Azure
  Functions host, Blob / Queue / Table storage, Cosmos-compatible local
  coverage where available, Key Vault-shaped secret references, and logs.

## Verification Boundary

Default example verification runs only unit / smoke tests and IaC isolation.
Local provider and real-cloud tests are explicit opt-in tiers because they
require containers, credentials, account quota, or may incur cost.

Local providers prove handler wiring, payload shape, idempotency persistence,
and provider API usage. Ephemeral real cloud proves IAM, trigger delivery,
packaging, service limits, and managed-service behavior.
