# Scenario Router

The scenario router decides which excellent-catalog-derived workload pattern is active, then loads scenario material that helps choose archetype, manifest, support services, and canonical examples. It does not override explicit provider, runtime, language, or IaC choices; it translates business-shaped prompts into cloud-shaped profiles.

## Core Rule

Match the workload topology and managed-service seams before matching provider names.

## Mappings / Signals

- "image moderation", "receipt ocr", "object upload enrichment", "blob intake", "gcs intake", "s3 intake", "document arrives in storage"
  - load `context/scenarios/function-scenarios.md`
  - scenario pattern `function.object-intake-enrichment`
- "stripe webhook", "signed webhook", "return 202", "dedupe webhook"
  - load `context/scenarios/function-scenarios.md`
  - scenario pattern `function.signed-webhook-orchestrator`
- "queue worker", "document translation", "classification queue", "support queue"
  - load `context/scenarios/function-scenarios.md`
  - scenario pattern `function.queue-backed-worker`
- "cdc relay", "change feed", "stream to search", "pub/sub fan-out"
  - load `context/scenarios/function-scenarios.md`
  - scenario pattern `function.change-event-relay`
- "public api and private worker", "nightly job", "claims intake", "permit workflow", "partner gateway"
  - load `context/scenarios/container-scenarios.md`
  - scenario pattern `container.public-api-private-worker-job`
- "custom binary", "headless chrome", "ffmpeg", "gdal", "libreoffice", "large document rendering"
  - load `context/scenarios/container-scenarios.md`
  - scenario pattern `container.heavy-runtime-service`
- "sidecar", "otel collector sidecar", "envoy sidecar"
  - load `context/scenarios/container-scenarios.md`
  - scenario pattern `container.multi-container-sidecar`
- "api plus workers plus jobs plus crons", "replay jobs", "multi-role", "separate scaling and recovery"
  - load `context/scenarios/kubernetes-scenarios.md`
  - scenario pattern `k8s.multi-role-platform`
- "rag knowledge mesh", "embedding workers", "vector rebuild job", "freshness scan"
  - load `context/scenarios/kubernetes-scenarios.md`
  - scenario pattern `k8s.rag-knowledge-mesh`

## Stop Conditions

- Stop when the prompt names only a provider service with no workload topology, such as "use S3" or "use Cosmos".
- Stop when two scenario patterns tie and would imply different runtime tiers; ask whether the repo should be function, managed-container, or k8s.
- Stop when a business prompt requires a managed-service seam that has no provider-native or declared bring-your-own equivalent.
- Stop when scenario inference conflicts with an explicit runtime choice and the user has not said to revise that choice.

## Routing Examples

- "build a moderated upload flow" -> `function.object-intake-enrichment`
- "claims intake API with private review worker and nightly escalation" -> `container.public-api-private-worker-job`
- "clickstream platform with APIs, Kafka workers, replay jobs, and export crons" -> `k8s.multi-role-platform`
- "use Cosmos for records" -> no scenario; continue with provider/runtime/stack routing

