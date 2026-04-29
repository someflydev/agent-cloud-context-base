# Managed Container Multi Service

Use this archetype for a small managed-container system with a public API, private worker or callback service, and a scheduled or event-driven job. It keeps the managed-container tier while acknowledging that the service topology, eventing seam, and private network path are now part of the durable repo shape.

## Common Goals

- Separate public API, private worker, and job runtime responsibilities.
- Keep each service image aligned with its own runtime needs.
- Add provider-native eventing with DLQ and replay behavior.
- Keep private services unreachable from the public internet.
- Test representative cross-service flows in the dev/test isolated stack.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/container-image-discipline.md`
- `context/doctrine/vpc-and-private-networking.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+managed-container stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-cloudrun/`, `examples/canonical-apprunner/`, or `examples/canonical-aca/`

## Common Workflows

- `context/workflows/add-managed-container-service.md`
- `context/workflows/add-cloud-runtime-image.md`
- `context/workflows/add-eventing-seam.md`
- `context/workflows/add-replay-and-dlq-handling.md`
- `context/workflows/add-vpc-private-network-path.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-cloud-integration-tests.md`

## Likely Manifests

- `manifests/container-cloudrun-fastapi.yaml`
- `manifests/container-apprunner-fastapi.yaml`
- `manifests/container-aca-jobs.yaml`

## Likely Examples

- `examples/canonical-cloudrun/public-api-private-worker-job/`
- `examples/canonical-apprunner/partner-adapter-with-worker/`
- `examples/canonical-aca/api-worker-scheduled-job/`

## Typical Anti-Patterns

- Exposing private workers to the public internet.
- Sharing one image across services with different runtime needs.
- Calling an eventing path complete without DLQ and replay.
- Letting a scheduled job mutate state without an idempotent run key.
- Expanding into many independent services without reconsidering Kubernetes.

## Validation Gates (summary)

- container-image-buildable: All images build clean.
- container-health-and-readiness: Public and private services respond to probes.
- container-private-network-when-required: Private worker is unreachable from the public internet.
- eventing-dlq-path: DLQ destination, alarm, and replay path are verified.
