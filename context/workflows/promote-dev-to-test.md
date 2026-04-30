# Promote Dev To Test

Use this workflow when promoting a verified dev change into the test environment for cloud resources, workloads, or Kubernetes overlays.

## Preconditions

- Dev validation has passed or skipped checks are explicitly recorded as `incomplete`.
- Test state, names, secret paths, identities, and env-var prefixes are disjoint from dev.
- The operator accepts any cost or quota impact of applying test resources.

## Sequence

1. Confirm the dev IaC plan or Pulumi preview is clean.
2. Confirm the change has smoke or integration evidence in dev.
3. Run the test workspace, stack, overlay, or environment apply.
4. Run `python3 scripts/validate_iac_isolation.py <path>` where available.
5. Run smoke tests against test.
6. Run integration tests against test for the changed boundary.
7. Confirm event queues, topics, and DLQs are healthy and DLQs are empty unless the test intentionally filled them.
8. Check logs, metrics, and traces for the promoted path when observability is in scope.
9. Record completion as `done`, `incomplete`, or `blocked` with exact commands.

## Outputs

- Test environment updated to match the promoted dev change.
- Promotion evidence from plan/preview, isolation validation, tests, and DLQ checks.

## Validation Gates

- `iac-plan-clean` from `profile-rules.json`
- `iac-dev-test-disjoint`
- `changed-boundary-proof`
- `eventing-dlq-path`

## Related Docs

- `context/doctrine/multi-environment-promotion.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/stacks/iac-pulumi-typescript.md`

## Common Pitfalls

- Applying test before confirming dev has no drift.
- Reusing dev secrets or identities during the promotion.
- Forgetting to inspect DLQs after event-driven test runs.
