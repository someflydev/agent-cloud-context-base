# AWS Lambda TypeScript Node

Load this stack for AWS Lambda functions written in TypeScript on Node.js. It owns esbuild packaging, AWS SDK v3 usage, handler contracts, and function-specific event discipline for accb Lambda workloads.

## Runtime Surface

- Runtime pin: Node.js 20 on AWS Lambda.
- Packaging: esbuild bundle to zip; exclude AWS SDK clients only when the runtime-provided version is acceptable, otherwise bundle explicit v3 clients.
- Dependency tool: npm, pnpm, or bun follows the generated repo choice; keep the Lambda bundle deterministic.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; keep top-level imports narrow.
- Limits: keep request-path timeout under 30s; declare any use of the 15 minute maximum; size memory from measured CPU and network behavior.
- Supported triggers: S3, DynamoDB Streams, SQS, SNS, EventBridge rules, EventBridge Scheduler, API Gateway REST, API Gateway HTTP, API Gateway WebSocket, Cognito triggers, Kinesis, IoT, CloudWatch Logs subscriptions, CodePipeline events.

## Project Layout

```
src/
  handler.ts
  events.ts
  idempotency.ts
  settings.ts
tests/
  fixtures/events/
  unit/
  integration/
package.json
tsconfig.json
```

## Handler Skeleton

```typescript
import type { Context } from "aws-lambda";

type LambdaEvent = Record<string, unknown>;

export async function handler(event: LambdaEvent, context: Context) {
  return { ok: true, requestId: context.awsRequestId };
}
```

## Local Invocation

```bash
npm test -- tests/unit
npm test -- tests/integration/lambda-event.test.ts
```

## Idempotency Pattern

- Derive the dedupe key from S3 bucket/key/versionId, SQS messageId, SNS MessageId, EventBridge id, DynamoDB eventID, Kinesis eventID, API idempotency header, WebSocket connectionId plus message id, or Cognito userName plus triggerSource.
- Bind dedupe records to DynamoDB with environment, function name, dedupe key, status, effect checksum, and TTL.
- Keep accepted, duplicate, and failed attempts distinct for replay audit.
- Replay test command: `npm test -- tests/integration/idempotency-replay.test.ts`.

## Identity Binding

- Use one IAM execution role per function boundary unless a generated repo deliberately groups identical handlers.
- Scope AWS SDK v3 client permissions to exact resources and actions.
- Reference `context/stacks/identity-aws-iam.md` for the PROMPT_12 identity stack.

## Secrets

- Use AWS Secrets Manager; pass secret ARNs or names through environment variables and resolve values with AWS SDK v3.
- Avoid embedding secret JSON in environment variables.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-aws-secrets-manager.md`.

## Observability

- Emit JSON logs with `timestamp`, `level`, `service`, `env`, `awsRequestId`, `triggerType`, `dedupeKey`, and `outcome`.
- Propagate trace context from API Gateway headers, Lambda context, message attributes, or EventBridge trace headers.
- Use CloudWatch Embedded Metrics Format or `@aws-lambda-powertools/metrics` for trigger, duplicate, and error counters.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `lambda-handler-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Shipping the whole monorepo dependency tree into one Lambda bundle.
- Using broad `AWSLambdaBasicExecutionRole` plus wildcard resource access as the final policy.
- Treating API Gateway, queue, and stream events as the same contract.
- Performing irreversible effects before the dedupe write succeeds.
