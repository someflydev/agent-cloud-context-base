# Fix Bug

Use this workflow when correcting a regression or incorrect behavior in existing runtime, IaC, docs, validation, or context files.

## Preconditions

- The observed failure, expected behavior, and affected boundary are known.
- Reproduction command or minimal failing case exists or is created first.
- Any cloud-resource fix keeps dev/test isolation intact.

## Sequence

1. Reproduce the bug or capture the smallest failing evidence.
2. Identify the likely owner: runtime code, IaC, tests, docs, router, manifest, or generated payload.
3. Add or adjust a regression test before the fix when feasible.
4. Make the smallest behavior change that addresses the cause.
5. Keep unrelated cleanup out of the bug fix.
6. Verify positive behavior and any relevant negative path.
7. Run IaC plan/preview or isolation validation if cloud resources changed.
8. Update docs or memory only if the bug revealed a durable repo rule.
9. Mark completion `blocked` or `incomplete` if reproduction or verification cannot run.

## Outputs

- Minimal bug fix, regression coverage, and verification evidence.

## Validation Gates

- `changed-boundary-proof` from `profile-rules.json`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/testing-philosophy-cloud.md`
- `context/doctrine/stop-conditions.md`
- `context/stacks/iac-pulumi-go.md`

## Common Pitfalls

- Fixing the symptom while leaving the failing path untested.
- Expanding scope into refactor or new feature work.
- Ignoring IaC drift when the bug lives in cloud configuration.
