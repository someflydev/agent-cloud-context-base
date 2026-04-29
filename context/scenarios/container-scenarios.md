# Container Scenarios

Container scenarios cover managed-container workloads that need custom images or a small multi-service topology while still avoiding Kubernetes operations. The default isolation surface is separate dev/test state, env-var prefix, secret path, image tag namespace, service name, and eventing resources.

## public-api-private-worker-job

- Likely archetype: `managed-container-multi-service`.
- Provider-specific stack choices: Cloud Run service plus Cloud Run Job; App Runner service plus ECS task or EventBridge scheduled job; Container Apps plus Container Apps Job.
- Support services: managed SQL or document database, object storage, queue or topic, provider-native secrets, private networking where the worker is not public.
- IaC isolation defaults: dev/test state keys, image repositories or tags, service names, job names, queue names, and secret paths are disjoint.
- Validation gates: `container-image-buildable`, `container-health-and-readiness`, `container-private-network-when-required`, `eventing-dlq-path`.

## heavy-runtime-service

- Likely archetype: `managed-container-service`.
- Provider-specific stack choices: Cloud Run for request or job-style renderers; App Runner for steady public services; Container Apps for service or job variants.
- Support services: object storage for input/output artifacts, database for status, secret store for partner or model credentials, optional queue for async work.
- IaC isolation defaults: image tags, service names, artifact buckets or containers, status tables, and secret paths differ between dev and test.
- Validation gates: `container-image-buildable`, `container-health-and-readiness`, `storage-real-roundtrip-in-test-stack`, `secret-binding-via-identity`.

## partner-adapter-gateway

- Likely archetype: `managed-container-multi-service`.
- Provider-specific stack choices: Cloud Run with serverless VPC access; App Runner with VPC connector; Container Apps with VNet integration.
- Support services: private database or partner endpoint, signed archive storage, retry queue, DLQ, provider-native secrets.
- IaC isolation defaults: private connector names, subnet references, queue names, archive paths, and partner secret paths are environment-specific.
- Validation gates: `container-private-network-when-required`, `eventing-dlq-path`, `secret-binding-via-identity`, `identity-least-privilege-declared`.

## multi-container-sidecar

- Likely archetype: `managed-container-service` unless the sidecar participates in API, worker, and job topology, then `managed-container-multi-service`.
- Provider-specific stack choices: Cloud Run multi-container revision, Container Apps sidecar-enabled app, or provider-supported paired container runtime; App Runner requires a different pattern when sidecars are unsupported.
- Support services: OTel collector or logging sink, Envoy or proxy config, object upload helper, secret store.
- IaC isolation defaults: revision names, collector endpoints, proxy config, and secret paths are split by dev/test.
- Validation gates: `container-image-buildable`, `container-health-and-readiness`, `secret-binding-via-identity`, `changed-boundary-proof`.

## job-first-container

- Likely archetype: `managed-container-service` for one job or `managed-container-multi-service` when a public control API submits jobs.
- Provider-specific stack choices: Cloud Run Jobs, Container Apps Jobs, EventBridge scheduled ECS task, or provider batch primitive when the managed-container tier delegates compute.
- Support services: scheduler, object storage, status database, queue, secret store.
- IaC isolation defaults: job names, run-key namespace, schedules, storage prefixes, and status tables are disjoint.
- Validation gates: `container-image-buildable`, `storage-real-roundtrip-in-test-stack`, `function-idempotency-proof`, `iac-dev-test-disjoint`.
