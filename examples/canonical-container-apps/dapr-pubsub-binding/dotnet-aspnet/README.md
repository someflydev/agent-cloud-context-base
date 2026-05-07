# Container Apps Dapr pub/sub and bindings

.NET 8 ASP.NET seed for `accb` Azure Container Apps generation.

Flow: publisher Container App posts `/orders` -> Dapr pub/sub component backed
by a Service Bus topic -> subscriber Container App handles `/orders-handler`
-> Dapr state component backed by Cosmos DB. The Dapr secret store component
uses Key Vault through user-assigned managed identity. Both apps run in one
Container Apps environment and scope Dapr components to the apps that need
them.

Dev/test isolation surface:

- State: Terraform `dev` and `test` backends use distinct keys; Pulumi stacks
  are `dev` and `test`.
- Env-var prefix: `ACCB_ACA_DAPR_DEV_` and `ACCB_ACA_DAPR_TEST_`.
- Secret path: `/accb/dev/aca/dapr/component-secret` and
  `/accb/test/aca/dapr/component-secret`.
- Resource naming: `accb-${environment}-aca-dapr-*`.

Dapr is the right choice when eventing, state, secrets, and service invocation
need one component contract across multiple Container Apps or languages. It is
overkill for a single-component app that only needs one Azure SDK call and has
no cross-service building block contract to preserve.

Lane A runs the service container locally with a `miniblue` sidecar and local
Dapr component manifests. Azure-managed Dapr sidecar injection, managed
identity token exchange, component auth, and production Service Bus/Cosmos
behavior are Lane B.

Lane B creates isolated Azure test resources with `pulumi up --stack test`
and must be torn down immediately. Expected Lane B cost band: low, bounded by
one Container Apps environment, two apps with Dapr enabled, Service Bus topic,
Cosmos DB, Key Vault, ACR, Log Analytics, and managed identity.

Run default verification:

```bash
bash examples/canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet/tests/verify.sh
```
