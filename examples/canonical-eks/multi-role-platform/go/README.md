# EKS Multi-Role Platform (go)

This accb expansion demonstrates a Kubernetes multi-role platform for stream-enrichment in Go: ingest API, Kafka lag workers, replay job, scheduled S3 export.

Runtime roles:

- API: public ingress role with health and event ingestion endpoints.
- Worker: event-driven processor scaled by KEDA.
- Job: bounded replay/rebuild operation for recovery.
- CronJob: scheduled maintenance with `concurrencyPolicy: Forbid`.
- Control plane: cluster, workload identity, namespaces, autoscaling, and managed-service wiring.

IaC dev/test isolation:

- State: Terraform uses separate backend keys/prefixes for `dev` and `test`; Pulumi uses separate `dev` and `test` stacks.
- Env prefix: resources use `accb-aws-$env-multi-role-platform`.
- Secret paths: `/accb/eks/multi-role-platform/dev/workload` and `/accb/eks/multi-role-platform/test/workload`.
- Resource names: all cluster, identity, eventing, and storage names include the environment.

Managed services: MSK, S3, DynamoDB, IRSA, KEDA Kafka scaler.

Lane A runs on kind and replaces managed cloud services with `ministack` fakes. Lane B creates an ephemeral real EKS test cluster in an isolated test account/project/subscription and defaults to skipped unless `ACCB_RUN_REAL_CLOUD=1`; expected cost band is $5-$50 per run.
