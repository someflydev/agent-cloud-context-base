# Event Grid Alert Router - Python

Azure Functions Event Grid trigger that normalizes Azure Monitor alert events,
writes a routed incident document to Cosmos DB, and publishes a Service Bus
message to the owning operations topic. Idempotency is keyed by Event Grid event
id plus Azure resource id.

IaC dev/test isolation surface:

- State: Terraform uses `accb/azure-functions/eventgrid-alert-router/dev.tfstate`
  and `accb/azure-functions/eventgrid-alert-router/test.tfstate`; Pulumi uses
  separate `dev` and `test` stacks.
- Env-var prefix: `ACCB_AZURE_DEV_` and `ACCB_AZURE_TEST_`.
- Secret path: `/accb/dev/azure-functions/eventgrid-alert-router/` and
  `/accb/test/azure-functions/eventgrid-alert-router/` in Azure Key Vault references.
- Resource naming: every Azure resource includes the stack/environment suffix.

Lane A `miniblue` uses provider-shaped fakes for Event Grid, Cosmos DB, Service
Bus topics, and Key Vault references. Full managed Event Grid and Service Bus
proof is Lane B against an isolated Azure test subscription.
