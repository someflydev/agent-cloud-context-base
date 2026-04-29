# Managed Service Selection

Managed services are the default cloud boundary. Prefer the provider's operated service when it fits the workload, because generated repos should spend complexity on product behavior, not undifferentiated infrastructure.

## Prefer Provider Services

- Use Cognito, Identity Platform, or Entra ID for user and workload identity.
- Use Secrets Manager, Secret Manager, or Key Vault for secrets.
- Use EventBridge, SQS, SNS, Pub/Sub, Service Bus, or Event Grid for eventing.
- Use S3, GCS, or Blob Storage for object storage.
- Use DynamoDB, Firestore, or Cosmos DB for document-shaped state.
- Use RDS, Cloud SQL, or Azure SQL for relational records.

## Choose Specialized Stores

- Use OpenSearch, Vertex AI Search, or Azure AI Search for search.
- Use OpenSearch, pgvector, Vertex Vector Search, or Azure AI Search for vector retrieval.
- Use Step Functions, Workflows, or Durable Functions for multi-step orchestration.
- Use CloudWatch with X-Ray, Cloud Operations, or Azure Monitor for observability.
- Keep managed-service choices aligned with the selected provider stack.

## Allow BYO Only With Cause

- Allow BYO infrastructure when cross-cloud portability is a stated requirement.
- Allow BYO when managed cost is expected to exceed the alternative by more than 5x.
- Allow BYO when a hard compliance constraint blocks the managed service.
- Do not choose BYO for familiarity alone.
- Do not introduce a service that lacks a stack pack without naming the gap.

## Document Deviations

- Record every managed-service deviation in the manifest.
- Name the rejected provider-native service.
- Name the operational owner of the BYO component.
- Add tests for the boundary that replaced the managed service.
- Revisit the decision when provider support or cost changes.
