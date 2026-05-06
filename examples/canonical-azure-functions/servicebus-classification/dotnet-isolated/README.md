# Service Bus Classification - .NET Isolated

.NET 8 isolated Azure Function that consumes a Service Bus queue, classifies the
ticket with Azure OpenAI, writes the enriched ticket to Cosmos DB, and publishes
to a Service Bus topic for the owning team. Retries and DLQ behavior follow the
eventing discipline: transient failures retry, poison messages move to DLQ with
the original message id and classification attempt count.

IaC dev/test isolation surface:

- State: Terraform uses `accb/azure-functions/servicebus-classification/dev.tfstate`
  and `accb/azure-functions/servicebus-classification/test.tfstate`; Pulumi uses
  separate `dev` and `test` stacks.
- Env-var prefix: `ACCB_AZURE_DEV_` and `ACCB_AZURE_TEST_`.
- Secret path: `/accb/dev/azure-functions/servicebus-classification/` and
  `/accb/test/azure-functions/servicebus-classification/` in Key Vault.
- Resource naming: every Azure resource includes the stack/environment suffix.

Lane A `miniblue` uses Azurite plus provider-shaped fakes for Service Bus,
Azure OpenAI, Cosmos DB, and Key Vault references. Full Service Bus and Azure
OpenAI proof is Lane B against an isolated Azure test subscription.

