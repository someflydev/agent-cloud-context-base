# GKE Multi-Role Platform (python)

This accb seed demonstrates a Kubernetes multi-role platform for rag-asset-pipeline: upload API, Pub/Sub workers, vector rebuild job, freshness cron.

Runtime roles:

- API: public ingress role with health and event ingestion endpoints.
- Worker: event-driven processor scaled by KEDA.
- Job: bounded replay/rebuild operation for recovery.
- CronJob: scheduled maintenance with `concurrencyPolicy: Forbid`.
- Control plane: cluster, workload identity, namespaces, autoscaling, and managed-service wiring.

IaC dev/test isolation:

- State: Terraform uses separate backend keys/prefixes for `dev` and `test`; Pulumi uses separate `dev` and `test` stacks.
- Env prefix: resources use `accb-gcp-$env-multi-role-platform`.
- Secret paths: `projects/accb/secrets/gke-multi-role-platform/dev/workload` and `projects/accb/secrets/gke-multi-role-platform/test/workload`.
- Resource names: all cluster, identity, eventing, and storage names include the environment.

Managed services: GCS, AlloyDB, Vertex Vector Search, GKE Workload Identity, KEDA Pub/Sub scaler.

Lane A runs on kind and replaces managed cloud services with `minisky` fakes. Lane B creates an ephemeral real GKE test cluster in an isolated test account/project/subscription and defaults to skipped unless `ACCB_RUN_REAL_CLOUD=1`; expected cost band is $5-$50 per run.
