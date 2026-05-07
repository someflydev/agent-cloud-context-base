# Kubernetes Canonical Arc

PROMPT_23 adds the k8s-tier seed platforms for accb:

- `examples/canonical-eks/multi-role-platform/python/` models a stream-enrichment EKS platform with API, KEDA-scaled Kafka worker, GPU-optional enrichment worker, replay job, scheduled S3 export, MSK, S3, DynamoDB, and IRSA.
- `examples/canonical-gke/multi-role-platform/python/` models a RAG asset pipeline on GKE Autopilot with upload API, Pub/Sub workers, vector-index rebuild job, freshness cron, GCS, AlloyDB, Vertex Vector Search, and GKE Workload Identity.
- `examples/canonical-aks/multi-role-platform/dotnet/` models a subscription-event hydrator on AKS with ASP.NET billing API, Service Bus worker, invoice rebuild job, month-close cron, Cosmos DB, Azure SQL, Service Bus, and AKS Workload Identity.

Each seed has Kustomize and Helm manifests, Terraform dev/test plus matching Pulumi-language IaC, kind Lane A, ephemeral real-cluster Lane B, replay idempotency tests, and cron concurrency checks. Deferred variants remain EKS Go, GKE Go, and AKS TypeScript for PROMPT_30.
