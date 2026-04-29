# AWS Lambda Go

Load this stack for AWS Lambda functions written in Go. It owns Go 1.22 handler shape, `aws-lambda-go` runtime usage, zip packaging for `provided.al2023`, and trigger boundary rules for accb Lambda workloads.

## Runtime Surface

- Runtime pin: Go 1.22 built for Linux on AWS Lambda `provided.al2023`.
- Packaging: compiled binary in zip with bootstrap entrypoint; layers only for shared assets or native sidecars that remain within Lambda limits.
- Dependency tool: Go modules.
- Cold-start budget: follow `context/doctrine/cold-start-and-runtime-selection.md`; keep init work small and deterministic.
- Limits: keep request-path timeout under 30s; document any use near the 15 minute Lambda maximum; set memory from measured CPU and IO needs.
- Supported triggers: S3, DynamoDB Streams, SQS, SNS, EventBridge rules, EventBridge Scheduler, API Gateway REST, API Gateway HTTP, API Gateway WebSocket, Cognito triggers, Kinesis, IoT, CloudWatch Logs subscriptions, CodePipeline events.

## Project Layout

```
cmd/function/main.go
internal/events/
internal/idempotency/
internal/settings/
tests/fixtures/events/
go.mod
go.sum
```

## Handler Skeleton

```go
package main

import (
	"context"

	"github.com/aws/aws-lambda-go/lambda"
)

func Handler(ctx context.Context, event map[string]any) (map[string]any, error) {
	return map[string]any{"ok": true}, nil
}

func main() {
	lambda.Start(Handler)
}
```

## Local Invocation

```bash
go test ./...
go test ./internal/idempotency -run Replay
```

## Idempotency Pattern

- Derive the dedupe key from S3 bucket/key/versionId, SQS messageId, SNS MessageId, EventBridge id, DynamoDB eventID, Kinesis eventID, API idempotency header, or Cognito userName plus triggerSource.
- Bind dedupe records to DynamoDB with environment, function name, dedupe key, status, effect checksum, and TTL.
- Keep context cancellation handling separate from duplicate detection.
- Replay test command: `go test ./... -run IdempotencyReplay`.

## Identity Binding

- Use a narrow IAM execution role for the compiled function and its exact resource set.
- Scope DynamoDB, S3, queue, stream, and secret access by ARN and action.
- Reference `context/stacks/identity-aws-iam.md` for the PROMPT_12 identity stack.

## Secrets

- Use AWS Secrets Manager; pass secret names or ARNs through configuration and read values through the AWS SDK for Go.
- Cache clients globally; cache secret values only within rotation tolerance.
- Default rotation cadence: 90 days unless the upstream credential requires shorter rotation.
- Reference `context/stacks/secrets-aws-secrets-manager.md`.

## Observability

- Emit structured JSON logs with `timestamp`, `level`, `service`, `env`, `aws_request_id`, `trigger_type`, `dedupe_key`, and `outcome`.
- Propagate trace context from context values, HTTP headers, message attributes, or EventBridge metadata.
- Emit CloudWatch Embedded Metrics Format for accepted, duplicate, retryable, and terminal outcomes.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `lambda-handler-contract` from `context/accb/profile-rules.json`.
- `function-idempotency-proof` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Using reflection-heavy generic event parsing when provider event structs exist.
- Letting background goroutines outlive the invocation contract.
- Treating local `/tmp` as durable workflow state.
- Building on a developer workstation target instead of Linux Lambda target.
