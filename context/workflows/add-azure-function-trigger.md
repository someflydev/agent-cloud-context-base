# Add Azure Function Trigger

Use this workflow when adding an Azure Functions workload with an HTTP, Blob, Queue, Service Bus, Event Grid, Event Hubs, Cosmos, or Timer trigger.

## Preconditions

- Azure is the selected provider and Azure Functions is the runtime tier.
- Trigger type, binding model, runtime language, and IaC tool are chosen.
- Dev/test state, app names, env-var prefixes, Key Vault paths, managed identities, and resource groups are disjoint.

## Sequence

1. Identify the binding payload shape and whether the project uses the v4 or v2 programming model for the language.
2. Author the function entry point with the correct decorators, bindings, and startup model.
3. Declare the function app, storage account, trigger source, managed identity, Key Vault references, and failure destination in IaC.
4. Scope identity permissions to the trigger source, target resources, dedupe store, and DLQ-equivalent destination.
5. Declare the idempotency key from event id, blob version, queue message id, partition event, timer slot, or business key.
6. Add unit tests for parsing, validation, and pure logic.
7. Add smoke tests that invoke the binding shape or local function host entry point.
8. Add Lane A Azurite/emulator or Lane B ephemeral real integration tests for trigger, effect, retry, and failure routing.
9. Run `terraform plan` or `pulumi preview` for dev and test before marking completion.

## Outputs

- Azure Function entry point, binding fixture, IaC resources, managed identity, failure path, and tests.

## Validation Gates

- `azure-fn-trigger-contract` from `profile-rules.json`
- `function-idempotency-proof`
- `eventing-dlq-path`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/trigger-boundary-discipline.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/stacks/azure-fn-python.md`
- `examples/canonical-azure-functions/blob-trigger-receipt-ocr/`

## Common Pitfalls

- Copying connection strings into app settings instead of using managed identity and Key Vault references.
- Confusing poison queues, dead-letter queues, and Event Grid retry semantics.
- Testing only the function method while ignoring binding startup.
