# Post Flight Refinement

Use this workflow when a bounded change is functionally complete and needs final cleanup before commit or handoff.

## Preconditions

- The main implementation work is complete.
- Required validation has run or the skipped commands are documented.
- No unrelated dirty worktree changes are reverted or absorbed accidentally.

## Sequence

1. Review changed files and separate intended edits from unrelated worktree state.
2. Run formatting or linting commands appropriate to the touched files.
3. Remove temporary notes, debug output, and unused scaffolding.
4. Confirm generated docs, router references, manifests, and examples still point at existing files.
5. Rerun the smallest validation command that proves the changed boundary.
6. Check for forbidden naming, secret leaks, and stale `.accb/` references.
7. Update memory or session state only when durable context changed.
8. Prepare a concise summary of changes, validation, and residual risk.
9. Stop before commit unless the operator asked for a commit.

## Outputs

- Cleaned change set ready for commit or handoff.
- Final validation and risk summary.

## Validation Gates

- `changed-boundary-proof` from `profile-rules.json`
- `secret-not-in-source`
- `startup-rehydration`

## Related Docs

- `context/doctrine/core-principles.md`
- `context/doctrine/naming-and-clarity.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Reformatting unrelated files during final cleanup.
- Removing user changes while trying to tidy the worktree.
- Forgetting to rerun validation after cleanup edits.
