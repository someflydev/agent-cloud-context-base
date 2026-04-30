# Add Cloud Function

Use this workflow when the request is to add a cloud function but the provider-specific trigger workflow must be selected before handler, IaC, and tests can be authored.

## Preconditions

- Provider is chosen as AWS, GCP, or Azure.
- Runtime language and IaC tool are known.
- Dev/test isolation is declared before any function, trigger, secret, or identity resource is generated.

## Sequence

1. Confirm the provider choice and route to the matching provider trigger workflow.
2. For AWS Lambda, load `context/workflows/add-aws-lambda-trigger.md`.
3. For GCP Cloud Functions Gen2, load `context/workflows/add-gcp-cloud-function-trigger.md`.
4. For Azure Functions, load `context/workflows/add-azure-function-trigger.md`.
5. Keep this workflow as the generic entry point and let the provider workflow own handler shape.
6. Load the relevant IaC stack and identity stack for the provider.
7. Confirm idempotency and retry expectations before code generation.
8. Add unit, smoke, and integration coverage at the cheapest layer that proves the new boundary.

## Outputs

- A routed provider-specific function workflow.
- A function implementation plan that includes handler, trigger, IaC, identity, idempotency, and tests.

## Validation Gates

- `function-trigger-contract` from `profile-rules.json`
- `function-idempotency-proof`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/trigger-boundary-discipline.md`
- `context/doctrine/idempotency-and-replay.md`
- `context/stacks/aws-lambda-python.md`

## Common Pitfalls

- Writing a generic handler that ignores provider payload shape.
- Adding a trigger without a DLQ or replay decision.
- Treating provider choice as implied by the user's local SDK preference.
