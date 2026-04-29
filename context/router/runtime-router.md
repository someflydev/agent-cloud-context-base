# Runtime Router

The runtime router decides whether the workload should use a function, a managed container, or Kubernetes. It does not choose provider, language, IaC tool, specific stack file, or archetype; it only classifies the runtime tier implied by workload shape and operational needs.

## Core Rule

Select the lowest runtime tier that satisfies the workload contract, and escalate only when trigger shape, binaries, duration, topology, scaling, or isolation requirements make the current tier insufficient.

## Mappings / Signals

- thin trigger, one transformation step, one persistence step
  - runtime tier `function`
- provider time and memory limits are acceptable
  - runtime tier `function`
- cold-start budget is tolerated
  - runtime tier `function`
- no custom binaries or heavyweight runtime dependencies
  - runtime tier `function`
- S3, GCS, Blob, Pub/Sub, Event Grid, EventBridge, queue, webhook, or scheduler edge
  - runtime tier `function`
- custom binaries such as `ffmpeg`, `GDAL`, Chrome, or LibreOffice
  - runtime tier `managed-container`
- one service or a small bounded set of companions
  - runtime tier `managed-container`
- steady traffic where cold starts hurt the user-facing contract
  - runtime tier `managed-container`
- jobs and cron run alongside an API without a full platform control plane
  - runtime tier `managed-container`
- sidecars such as OpenTelemetry collector or Envoy are useful and supported by the target platform
  - runtime tier `managed-container`
- API plus worker fleet plus jobs plus crons plus control-plane behavior
  - runtime tier `k8s`
- multi-tenant namespace isolation, mesh policy, KEDA-style scaling, or independent rollout contracts
  - runtime tier `k8s`
- heavy compute classes with separate CPU, GPU, and memory tiers
  - runtime tier `k8s`
- rolling rollout and rollback contracts not supplied by the managed-container platform
  - runtime tier `k8s`

## Stop Conditions

- Stop when more than one runtime tier is plausible and the deciding trigger, duration, binary, traffic, topology, or isolation fact is missing.
- Stop when the prompt asks for Kubernetes but gives no topology reason and a managed container would satisfy the stated behavior.
- Stop when the request implies both a function trigger contract and a long-running custom runtime with no declared split.
- Stop when runtime escalation would change identity, network, observability, or test boundaries and the user has not accepted that change.

## Routing Examples

- "process each S3 object upload and write a DynamoDB record" -> `function`
- "render PDFs with headless Chrome behind an HTTP API" -> `managed-container`
- "claims intake API with private worker and nightly escalation job" -> `managed-container`
- "API plus Kafka workers, replay jobs, export crons, and namespace isolation" -> `k8s`

