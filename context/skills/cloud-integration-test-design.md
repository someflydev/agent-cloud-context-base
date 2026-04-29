# Cloud Integration Test Design

Use this skill to choose an integration test lane for cloud boundaries: Lane A emulator, Lane B ephemeral real infrastructure, or Lane C record/replay. It resolves ambiguity by comparing emulator fidelity, real-cloud cost, fixture flakiness, profile size, and the managed-service semantics under test.

## Procedure

1. Identify the cloud boundary under test: trigger, storage, database, eventing, secrets, identity, network, or observability.
2. Assess emulator quality for the selected provider service and the specific semantics being exercised.
3. Assess the cost, quota pressure, setup time, and teardown reliability of ephemeral real infrastructure.
4. Assess whether record/replay fixtures would become stale or hide provider behavior.
5. Prefer Lane B for medium and larger profiles where managed-service semantics are part of the contract.
6. Use Lane A for cheap local feedback when emulator behavior matches the tested contract.
7. Use Lane C for expensive, slow, or hard-to-create boundaries when fixtures are clearly versioned and refreshed.
8. Combine A and C for cheap scenarios that need local speed plus deterministic edge cases.
9. Define teardown, naming, and test isolation before running real-cloud tests.
10. Stop if the selected lane cannot prove the boundary that the manifest claims to validate.

## Good Triggers

- "integration test lane"
- "LocalStack or real AWS?"
- "use emulator?"
- "ephemeral test stack"
- "record/replay fixtures"
- "cloud smoke test is not enough"

## Avoid

- using mocks to claim managed-service integration
- choosing an emulator for semantics it does not implement
- creating real test resources without teardown and test naming
- allowing stale recorded fixtures to replace provider behavior silently
- skipping duplicate-delivery or replay tests for eventing boundaries
