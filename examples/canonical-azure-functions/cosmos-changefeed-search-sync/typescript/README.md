# Cosmos Change Feed Search Sync - TypeScript

TypeScript Azure Function that consumes Cosmos DB Change Feed events, transforms
product documents, updates an Azure AI Search index, and sends failed updates to
a Service Bus retry queue. Idempotency is keyed by Cosmos `_etag`.

IaC dev/test isolation surface:

- State: Terraform uses `accb/azure-functions/cosmos-search-sync/dev.tfstate`
  and `accb/azure-functions/cosmos-search-sync/test.tfstate`; Pulumi uses
  separate `dev` and `test` stacks.
- Env-var prefix: `ACCB_AZURE_DEV_` and `ACCB_AZURE_TEST_`.
- Secret path: `/accb/dev/azure-functions/cosmos-search-sync/` and
  `/accb/test/azure-functions/cosmos-search-sync/` in Key Vault references.
- Resource naming: every Azure resource includes the stack/environment suffix.

Lane A `miniblue` uses provider-shaped fakes for Cosmos Change Feed, Azure AI
Search, Service Bus retry queues, and Key Vault references. Full managed search
and Service Bus proof is Lane B against an isolated Azure test subscription.

