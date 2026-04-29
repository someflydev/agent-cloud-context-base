# Storage Azure Blob Cosmos Azure SQL

Load this stack for Azure storage in accb-derived repos. It owns Blob Storage, Cosmos DB, Azure SQL, lifecycle, private endpoints, managed identity, and validation.

## Capability Surface

- Object storage: Azure Blob Storage.
- Multi-model database: Cosmos DB.
- Relational storage: Azure SQL.
- Dev names: `<repo>-dev-<store>`.
- Test names: `<repo>-test-<store>`.
- Dev secret prefix: `<repo>-dev-storage-`.
- Test secret prefix: `<repo>-test-storage-`.
- Reference `context/doctrine/iac-dev-test-isolation.md`.

## Blob Pattern

- Enable secure transfer.
- Disable public access unless a manifest waiver exists.
- Use lifecycle rules for tiering and expiration.
- Enable soft delete when recovery is required.
- Enable immutability policies for records that require retention locks.
- Use Event Grid notifications deliberately.
- Prefer managed identity over account keys.

## Cosmos DB Pattern

- Choose API surface explicitly.
- Select consistency level from workload requirements.
- Define partition keys from access patterns.
- Avoid hot logical partitions.
- Use change feed only when downstream processing is declared.
- Set throughput mode deliberately.
- Use private endpoints when network isolation is required.

## Azure SQL Pattern

- Choose DTU or vCore model explicitly.
- Prefer vCore for production-shaped examples.
- Use private endpoint when private workloads require it.
- Store credentials in Key Vault.
- Prefer managed identity authentication where supported.
- Run migrations through application workflow.
- Configure auditing when required by the platform.

## Identity Binding

- Grant Blob data roles at container or account scope.
- Grant Cosmos DB data-plane roles where supported.
- Grant Azure SQL access through managed identity or scoped credentials.
- Keep Key Vault secret access separate from data access.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## CLI Surface

```bash
az storage account show --name <account> --resource-group <rg>
az cosmosdb show --name <account> --resource-group <rg>
az sql db show --server <server> --name <db> --resource-group <rg>
```

## Observability

- Track Blob request errors, capacity, and latency.
- Track Cosmos DB request units, throttles, consistency, and partition hot spots.
- Track Azure SQL DTU or vCore metrics, connections, deadlocks, and storage.
- Include resource, environment, tenant, request ID, and trace ID in logs.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates

- Dev and test storage resources differ.
- Public access is disabled unless waived.
- Partition keys are declared for Cosmos DB.
- Database credentials live in Key Vault.
- Private endpoint choice is documented.

## Anti-Patterns

- Account keys in app settings.
- Shared database for dev and test.
- Cosmos DB partition key chosen after launch.
- Blob containers public by default.
- Storage events without idempotent consumers.
