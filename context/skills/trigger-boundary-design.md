# Trigger Boundary Design

Use this skill to keep function handlers thin when a trigger could absorb business workflow, heavy processing, or stateful orchestration. It resolves boundary ambiguity by separating trigger payload handling, side effects, and work that belongs in containers, jobs, or workflow services.

## Procedure

1. Identify the trigger source and the provider payload shape.
2. Enumerate the required trigger fields: source id, event time, object or record key, tenant, correlation id, and retry metadata.
3. Enumerate side effects: storage read, validation, enrichment, durable write, fan-out publish, secret access, and operator notification.
4. Classify each side effect as required before ack, safe after ack, or recoverable through retry and DLQ.
5. Identify anything that requires more than 5 seconds, more than 256MB, custom binaries, or stateful coordination.
6. Move heavy or stateful work into a managed container, job, workflow service, or downstream worker.
7. Keep the handler focused on validation, idempotency key derivation, minimal transformation, durable state transition, and event publication.
8. Document the ack point and retry behavior with DLQ handling.
9. Add tests for malformed payloads, duplicate delivery, retryable failure, and side-effect idempotency.

## Good Triggers

- "keep the handler thin"
- "where should this logic live?"
- "trigger boundary"
- "Lambda does too much"
- "function handler design"
- "move work out of the function"

## Avoid

- placing multi-step orchestration directly in a trigger handler
- doing large binary processing inside a function without evidence it fits
- acking before the durable state transition is safe
- hiding side effects behind helper calls with no retry or idempotency contract
- treating a DLQ as optional for event-driven work
