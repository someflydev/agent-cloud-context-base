# Assistant Behavior Spec

## MUST

- Read `AGENT.md` and run `python3 scripts/work.py resume` at session start in `accb`.
- In generated repos, read `.accb/SESSION_BOOT.md` and `.accb/profile/selection.json`.
- Declare provider, runtime tier, language, IaC tool, manifest, support services, and dev/test isolation before generating cloud resources.
- Prefer manifest-defined bundles over improvised context loading.
- Run relevant validation before saying `done`.
- Use `blocked`, `incomplete`, and `done` precisely.

## SHOULD

- Load one router, one workflow, one stack, one archetype, one scenario pattern, and one canonical example before broadening.
- Choose canonical examples before inventing new patterns.
- Keep local runtime notes in `context/SESSION.md` or `context/MEMORY.md`, not in doctrine.
- Update `.accb/` payloads when profile truth changes.

## Validation Status Vocabulary

`done` means proof ran and passed. The proof may be a context validator, manifest validator, IaC isolation check, example verifier, generated repo `accb_verify`, smoke test, or explicitly scoped parity runner.

`incomplete` means work progressed but required proof has not run or has not passed yet.

`blocked` means the next required proof or change cannot proceed without missing credentials, unavailable local services, operator input, cloud quota, or a policy decision.
