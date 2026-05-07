# AKS Multi-Role Platform (dotnet)

This accb seed demonstrates a Kubernetes multi-role platform for subscription-event-hydrator: billing API, Service Bus worker, invoice rebuild job, month-close cron.

Runtime roles:

- API: public ingress role with health and event ingestion endpoints.
- Worker: event-driven processor scaled by KEDA.
- Job: bounded replay/rebuild operation for recovery.
- CronJob: scheduled maintenance with `concurrencyPolicy: Forbid`.
- Control plane: cluster, workload identity, namespaces, autoscaling, and managed-service wiring.

IaC dev/test isolation:

- State: Terraform uses separate backend keys/prefixes for `dev` and `test`; Pulumi uses separate `dev` and `test` stacks.
- Env prefix: resources use `accb-azure-$env-multi-role-platform`.
- Secret paths: `https://accb-kv.vault.azure.net/secrets/aks-multi-role-platform/dev/workload` and `https://accb-kv.vault.azure.net/secrets/aks-multi-role-platform/test/workload`.
- Resource names: all cluster, identity, eventing, and storage names include the environment.

Managed services: Cosmos DB, Azure SQL, Service Bus, AKS Workload Identity, KEDA Service Bus scaler.

Lane A runs on kind and replaces managed cloud services with `miniblue` fakes. Lane B creates an ephemeral real AKS test cluster in an isolated test account/project/subscription and defaults to skipped unless `ACCB_RUN_REAL_CLOUD=1`; expected cost band is $5-$50 per run.
