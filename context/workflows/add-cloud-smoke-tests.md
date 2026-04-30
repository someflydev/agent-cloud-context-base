# Add Cloud Smoke Tests

Use this workflow when adding fast smoke tests for a function, managed container, or Kubernetes workload entry point.

## Preconditions

- Workload type and smoke boundary are known.
- Representative trigger, request, health, or readiness fixture exists or can be authored.
- Smoke tests can run in seconds without provisioning new cloud infrastructure.

## Sequence

1. Pick the smoke layer for the workload type.
2. For functions, invoke the handler with a real event fixture and mocked managed-service clients.
3. For containers, build or run the image and exercise health, readiness, and one representative route.
4. For Kubernetes, assert rendered probes and pod readiness or job invocation against the chosen test target.
5. Keep smoke assertions focused on entry point shape, startup, and one happy path.
6. Avoid cloud credentials unless the smoke boundary explicitly requires a deployed endpoint.
7. Add the command to the repo's verification notes or `.accb/` validation contract.
8. Make failures actionable with fixture names and expected response shape.
9. Run the smoke command locally before marking completion.

## Outputs

- Fast smoke test files and a runnable smoke command for the changed workload.

## Validation Gates

- `changed-boundary-proof` from `profile-rules.json`
- `function-trigger-contract`
- `container-health-and-readiness`
- `k8s-role-separation-evident`

## Related Docs

- `context/doctrine/testing-philosophy-cloud.md`
- `context/doctrine/trigger-boundary-discipline.md`
- `context/stacks/aws-lambda-typescript-node.md`

## Common Pitfalls

- Calling a smoke test an integration test because it uses provider-shaped fixtures.
- Letting smoke tests provision cloud resources by default.
- Adding many assertions that belong in unit or integration tests.
