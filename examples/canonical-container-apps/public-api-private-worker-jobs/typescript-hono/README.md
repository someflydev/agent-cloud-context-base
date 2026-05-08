# Container Apps public API, private worker, and jobs (TypeScript Hono)

TypeScript Hono seed for `accb` Azure Container Apps generation.

Flow: public Container App receives `/submit` -> Cosmos DB workflow state ->
Blob Storage attachments -> Service Bus work queue -> internal-only worker
Container App -> Service Bus triggered Container Apps Job for batch retry.
Key Vault app secrets are referenced through user-assigned managed identity.
The worker and job declare KEDA Service Bus scale rules on queue depth.

Dev/test isolation surface:

- State: Terraform `dev` and `test` backends use distinct keys; Pulumi stacks
  are `dev` and `test`.
- Env-var prefix: `ACCB_ACA_PUBLIC_WORKER_TYPESCRIPT_DEV_` and
  `ACCB_ACA_PUBLIC_WORKER_TYPESCRIPT_TEST_`.
- Secret path: `/accb/dev/aca/public-worker-typescript/api-key` and
  `/accb/test/aca/public-worker-typescript/api-key`.
- Resource naming: `accb-${environment}-aca-public-worker-typescript-*`.

Lane A runs the service container locally with a `miniblue` sidecar for Blob,
Service Bus-shaped, Cosmos-compatible, Key Vault-shaped, and log coverage.
Provider behavior not represented by `miniblue`, including managed identity
token exchange, ACR pulls, ACA internal ingress, and production KEDA scaler
authentication, is Lane B.

Lane B creates isolated Azure test resources with `pulumi up --stack test`
and must be torn down immediately. Expected Lane B cost band: low, bounded by
one Container Apps environment, two apps, one job, Service Bus, Cosmos DB,
Blob Storage, Key Vault, ACR, Log Analytics, and managed identity.

Run default verification:

```bash
bash examples/canonical-container-apps/public-api-private-worker-jobs/typescript-hono/tests/verify.sh
```
