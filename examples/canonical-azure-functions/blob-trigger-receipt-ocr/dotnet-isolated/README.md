# Blob Trigger Receipt OCR - .NET Isolated

.NET 8 isolated Azure Function for Blob Storage create events. The handler sends
receipt blobs to Azure AI Document Intelligence, writes normalized receipts to
Cosmos DB, and emits an Event Grid completion event. Idempotency is keyed by
blob name plus blob version or ETag.

IaC dev/test isolation surface:

- State: Terraform uses `accb/azure-functions/blob-receipt-ocr/dev.tfstate`
  and `accb/azure-functions/blob-receipt-ocr/test.tfstate`; Pulumi uses
  separate `dev` and `test` stacks.
- Env-var prefix: `ACCB_AZURE_DEV_` and `ACCB_AZURE_TEST_`.
- Secret path: `/accb/dev/azure-functions/blob-receipt-ocr/` and
  `/accb/test/azure-functions/blob-receipt-ocr/` in Azure Key Vault.
- Resource naming: every Azure resource includes the stack/environment suffix.

Lane A `miniblue` runs Azurite plus provider-shaped fakes for Document
Intelligence, Cosmos DB, Event Grid, and Key Vault references. Full managed
service proof is Lane B against an isolated Azure test subscription.
