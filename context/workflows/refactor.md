# Refactor

Use this workflow when changing code or docs structure without intentionally changing externally visible behavior.

## Preconditions

- Current behavior and verification commands are understood.
- The refactor has a bounded target and does not hide a feature or bug fix.
- Cloud resource naming, state, secrets, and identities are not changed unless explicitly part of the refactor.

## Sequence

1. State the behavior that must remain unchanged.
2. Identify the smallest files or modules that need restructuring.
3. Run or inspect current tests before changing risky behavior.
4. Move or reshape code in small steps while preserving public interfaces.
5. Update imports, docs, examples, and prompt references that point at moved files.
6. Avoid broad formatting churn outside the touched files.
7. Add focused regression tests if the refactor exposes an untested contract.
8. Run the relevant validation command after the refactor.
9. Record any remaining risk as `incomplete` if verification cannot run.

## Outputs

- Behavior-preserving code or documentation structure change.
- Updated references and focused verification evidence.

## Validation Gates

- `changed-boundary-proof` from `profile-rules.json`
- `startup-rehydration`

## Related Docs

- `context/doctrine/core-principles.md`
- `context/doctrine/testing-philosophy-cloud.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Combining refactor with feature work.
- Moving files without updating router, manifest, or prompt references.
- Claiming behavior preservation without running a relevant check.
