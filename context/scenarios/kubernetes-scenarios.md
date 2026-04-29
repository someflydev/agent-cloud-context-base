# Kubernetes Scenarios

Kubernetes scenarios cover workloads where topology, independent scaling, rollout behavior, tenancy, or heterogeneous compute warrants EKS, GKE, or AKS. If the request is only one API plus one worker, prefer managed containers until Kubernetes solves a current requirement.

## multi-role-platform

- Why k8s is warranted: API, worker, job, cron, and optional control-plane roles need independent rollout, probes, scaling, and identities.
- Role decomposition: API Deployment, worker Deployment with queue scaling, Job for bounded backfills, CronJob for schedules, optional control-plane Deployment.
- Provider cluster stack: EKS with IRSA or Pod Identity; GKE with Workload Identity; AKS with Workload Identity.
- Support services: queue or stream, database, object storage, secret manager, telemetry sink.
- Validation gates: `k8s-role-separation-evident`, `k8s-rolling-rollout-and-rollback-paths`, `k8s-worker-bounded-work-item`, `k8s-cron-execution`.

## stream-replay-platform

- Why k8s is warranted: sustained ingest, lag recovery, replay jobs, and export crons need separate scaling and operator-controlled backfill.
- Role decomposition: ingest API or consumer Deployment, stream worker Deployment, replay Job, export CronJob, admin control-plane Deployment.
- Provider cluster stack: EKS with MSK or SQS; GKE with Pub/Sub or Dataflow-adjacent services; AKS with Event Hubs or Service Bus.
- Support services: stream or queue, DLQ, checkpoint store, object export storage, secrets, telemetry.
- Validation gates: `k8s-role-separation-evident`, `eventing-dlq-path`, `k8s-job-completion`, `k8s-cron-execution`.

## rag-knowledge-mesh

- Why k8s is warranted: upload APIs, extraction workers, embedding workers, index rebuild jobs, and freshness scans scale and fail differently.
- Role decomposition: corpus API Deployment, extraction worker Deployment, embedding worker Deployment, index rebuild Job, freshness CronJob.
- Provider cluster stack: GKE with Vertex Vector Search, EKS with OpenSearch or external vector store, AKS with Azure AI Search.
- Support services: object storage, metadata database, vector store, model or embedding secret, queue, OTel telemetry.
- Validation gates: `rag-retrieval-sanity`, `k8s-role-separation-evident`, `k8s-job-completion`, `secret-binding-via-identity`.

## regulated-document-platform

- Why k8s is warranted: secure intake, malware scan, OCR, classification, review, audit, export, and retention jobs need strict role boundaries and policy.
- Role decomposition: intake API Deployment, malware/OCR/classification worker Deployments, review API Deployment, retention Job, export CronJob.
- Provider cluster stack: EKS, GKE, or AKS with workload identity, network policy, and provider-native audit/logging integrations.
- Support services: object storage with retention, database, queue, secret store, audit log sink, optional OCR or AI service.
- Validation gates: `k8s-role-separation-evident`, `identity-least-privilege-declared`, `secret-binding-via-identity`, `storage-real-roundtrip-in-test-stack`.

## workflow-control-plane

- Why k8s is warranted: a control API, scheduler, execution workers, reconciliation crons, and replay of failed steps need durable coordination and separate rollout.
- Role decomposition: control API Deployment, scheduler Deployment, executor worker Deployment, reconciliation CronJob, replay Job.
- Provider cluster stack: EKS, GKE, or AKS with provider-native queue, database, workload identity, and secret store.
- Support services: state database, queue, DLQ, object storage for artifacts, secret store, telemetry sink.
- Validation gates: `k8s-role-separation-evident`, `eventing-dlq-path`, `k8s-job-completion`, `k8s-cron-execution`.

## heterogeneous-compute-platform

- Why k8s is warranted: CPU, GPU, and high-memory worker classes need distinct node pools, scheduling constraints, resource requests, and rollout policy.
- Role decomposition: API Deployment, CPU worker Deployment, GPU worker Deployment, high-memory worker Deployment, batch Job, capacity scan CronJob.
- Provider cluster stack: EKS managed node groups, GKE node pools, or AKS node pools with taints, tolerations, and workload identity.
- Support services: queue, object storage, metadata database, secret store, image registry, metrics sink.
- Validation gates: `k8s-role-separation-evident`, `k8s-worker-bounded-work-item`, `k8s-job-completion`, `identity-least-privilege-declared`.
