# Trigger Boundary Discipline

Cloud functions are trigger edges, not miniature platforms. A function should validate an event, do one bounded transformation or orchestration step, and hand off heavier work to the cloud service designed to own it.

## Keep Functions Thin

- Validate the trigger payload at the boundary.
- Normalize provider event fields before they enter domain logic.
- Perform one bounded transformation, dispatch, or persistence step.
- Return clear success, retryable failure, or terminal failure.
- Keep the handler small enough that its contract is obvious.

## Hand Off Heavy Work

- Use managed containers for custom binaries such as ffmpeg, GDAL, or headless Chrome.
- Use Kubernetes jobs for long-running compute with separate scheduling and recovery needs.
- Use Step Functions, Workflows, or Durable Functions for multi-step orchestration.
- Use provider schedulers for scheduled invocation.
- Use managed queues and topics for fan-out or backpressure.

## Avoid Platform Drift

- Do not run long-lived loops inside a function.
- Do not host in-process queues inside a function runtime.
- Do not schedule background tasks from warmed function state.
- Do not perform heavy CPU or GPU work inside a trigger handler.
- Do not rely on local disk beyond documented ephemeral limits.

## Respect Provider Limits

- Check timeout, memory, payload, concurrency, and retry limits before choosing a function.
- Treat cold-start latency as part of the user-facing contract.
- Keep package size and dependency load time visible.
- Declare concurrency behavior for at-least-once triggers.
- Escalate when limits make the handler design brittle.

## Escalate Deliberately

- Move to a managed container when binaries, runtime shape, or request duration exceed function fit.
- Move to Kubernetes when multiple workload classes need separate scaling and recovery.
- Link the escalation to the function-vs-container-vs-k8s doctrine.
- Preserve the original trigger contract during escalation.
- Add tests for the new boundary before claiming completion.
