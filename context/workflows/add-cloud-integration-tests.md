# Add Cloud Integration Tests

Use this workflow when adding Lane A emulator, Lane B ephemeral real, or Lane C record/replay integration tests for a changed cloud boundary.

## Preconditions

- Manifest declares the intended integration lane.
- The changed boundary and required teardown behavior are known.
- Dev/test isolation exists for any real cloud resources.

## Sequence

1. Pick Lane A, Lane B, or Lane C according to the manifest and risk.
2. For Lane A, author LocalStack, GCP emulator, Azurite, or equivalent harness setup.
3. For Lane B, author `terraform apply`/`destroy`, Pulumi Automation API, or stack commands for ephemeral test resources.
4. For Lane C, record and replay only stable third-party API behavior with clear refresh instructions.
5. Assert the changed boundary end to end at the managed-service or emulator boundary.
6. Include duplicate delivery, retry, or permission checks when those are the changed risks.
7. Make teardown explicit and default to destroy for ephemeral real resources.
8. Add cost and quota notes when Lane B is used.
9. Run the integration command or mark completion `incomplete` with the skipped reason.

## Outputs

- Integration harness, test cases, teardown command, and lane declaration.

## Validation Gates

- `changed-boundary-proof` from `profile-rules.json`
- `storage-real-roundtrip-in-test-stack`
- `eventing-dlq-path`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/testing-philosophy-cloud.md`
- `context/doctrine/cost-and-quota-awareness.md`
- `context/stacks/iac-pulumi-python.md`

## Common Pitfalls

- Running a mocked client and labeling it integration.
- Creating Lane B resources without reliable teardown.
- Forgetting that permission failures are often the most important integration risk.
