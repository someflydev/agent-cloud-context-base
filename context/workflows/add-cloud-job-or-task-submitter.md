# Add Cloud Job Or Task Submitter

Use this workflow when adding a job or task submission boundary for cloud control-plane repos.

## Preconditions

- Provider job primitive or queue-backed task handoff is chosen.
- Submission request schema, caller identity, accepted states, and terminal failure states are known.
- Dev/test job resources, queues, identities, state, and secret paths are disjoint.

## Sequence

1. Choose the provider job primitive or queue-backed handoff for the runtime tier.
2. Define the request schema, validation errors, idempotency key, and accepted response shape.
3. Author IaC for job resources, queue or event seam, DLQ or terminal failure store, and identities.
4. Scope submitter identity separately from worker or executor identity.
5. Implement submission code that validates, records, and hands off work atomically.
6. Implement rejected submission behavior without creating partial cloud resources.
7. Add unit tests for schema validation and idempotency key behavior.
8. Add integration tests for accepted submission, rejected submission, duplicate submission, and terminal failure handling.
9. Add operator inspection commands for pending, running, failed, and completed work.

## Outputs

- Submission API or function, request schema, IaC job/event resources, identity bindings, terminal failure path, and tests.

## Validation Gates

- `identity-least-privilege-declared` from `profile-rules.json`
- `function-idempotency-proof`
- `eventing-dlq-path`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/idempotency-and-replay.md`
- `context/doctrine/eventing-and-dlq-discipline.md`
- `context/stacks/k8s-control-plane-workload.md`

## Common Pitfalls

- Letting a failed validation create a job or queue message.
- Reusing executor permissions for the submitter.
- Treating accepted submission as completed work.
