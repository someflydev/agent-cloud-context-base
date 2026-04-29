# Managed Service Substitution

Use this skill to translate a request written in one provider's vocabulary into the selected provider's native services. It resolves ambiguity by mapping abstract capabilities first and calling out semantic gaps instead of pretending that provider services are identical.

## Procedure

1. Identify the selected provider and the source provider vocabulary used in the prompt.
2. Extract the abstract capability: object storage, document store, relational database, queue, topic, event bus, stream, secret store, identity, search, vector retrieval, or orchestration.
3. Look up the provider-native equivalent in the relevant stack or managed-service doctrine.
4. Prefer the selected provider's operated service when it satisfies the workload.
5. Name semantic gaps explicitly, such as Cosmos DB change feed versus DynamoDB streams or Pub/Sub versus SQS visibility timeout behavior.
6. Determine whether the gap changes handler logic, retry behavior, ordering, replay, security, or tests.
7. If no provider-native equivalent fits, document the rejected managed service and the reason for bring-your-own infrastructure.
8. Update support services, manifest entries, identity permissions, and validation gates to match the substituted service.
9. Stop when the prompt requires a provider-specific semantic that the selected provider cannot provide.

## Good Triggers

- "translate S3 to Azure"
- "GCP equivalent of DynamoDB"
- "provider-native equivalent"
- "use the same architecture on another cloud"
- "what replaces Service Bus on AWS?"
- "map these services across providers"

## Avoid

- substituting by name without checking delivery, replay, consistency, or identity semantics
- keeping the old provider's terminology in generated resources
- introducing bring-your-own infrastructure without a documented reason
- ignoring stack packs for support services
- claiming two provider services are identical when the semantics differ
