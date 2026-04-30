# Add AWS Lambda Trigger

Use this workflow when adding an AWS Lambda function with a concrete trigger such as S3, SQS, DynamoDB Stream, EventBridge, API Gateway, or Cognito.

## Preconditions

- AWS is the selected provider and Lambda is the runtime tier.
- Trigger type, payload fixture, runtime language, and IaC tool are chosen.
- Dev/test state keys, env-var prefixes, secret paths, IAM role names, and resource names are disjoint.

## Sequence

1. Identify the exact AWS trigger payload shape and store a representative fixture.
2. Author the Lambda handler with clear parsing, validation, and error response behavior.
3. Declare the function, execution role, log group, trigger resource, permissions, and DLQ in IaC.
4. Scope IAM permissions to the trigger, target resources, dedupe store, and DLQ.
5. Declare the idempotency key strategy from event id, object version, message id, or business key.
6. Add unit tests for pure parsing, validation, and effect planning.
7. Add smoke tests that invoke the handler with the real event fixture and mocked managed clients.
8. Add Lane A LocalStack or Lane B ephemeral real integration tests for trigger, effect, retry, and DLQ behavior.
9. Run `terraform plan` or `pulumi preview` for dev and test before claiming completion.

## Outputs

- Lambda handler, trigger fixture, IaC resources, IAM role, DLQ, and tests.

## Validation Gates

- `lambda-handler-contract` from `profile-rules.json`
- `function-idempotency-proof`
- `eventing-dlq-path`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/trigger-boundary-discipline.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/stacks/aws-lambda-python.md`
- `examples/canonical-aws-lambda/s3-trigger-image-moderation/`

## Common Pitfalls

- Omitting `lambda:InvokeFunction` permissions from event source wiring.
- Sharing one IAM role across dev and test.
- Testing only direct handler calls when the risk is trigger mapping or retry.
