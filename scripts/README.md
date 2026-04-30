# Scripts

`scripts/` holds repo-local automation for `accb`.

## Implemented In PROMPT_05

- `work.py` — runtime continuity, prompt-state tracking, checkpointing, startup inspection, and graft support.

`work.py` subcommands:

- `init-project` — scaffold local runtime files from tracked `*.example.md` files.
- `resume` — print the Session Context Briefing.
- `checkpoint` — append a lightweight checkpoint under `work/`.
- `next` — print the next recommended prompt file.
- `start` — record that a prompt session started.
- `pause` — record that a prompt session paused with a reason.
- `done` — record that a prompt session completed with a summary.
- `recent-commits` — print the last ten commits with timestamps.
- `log-quota` — append a quota usage row.
- `verify` — run available structural verification scripts.
- `budget-report` — score a startup bundle when the feature gate is enabled.
- `route-check` — preview routing when the feature gate is enabled.
- `startup-trace` — write a startup trace when the feature gate is enabled.
- `graft` — install a minimal `.accb/` runtime continuity layer into a target repo.

## Planned For PROMPT_16

- `new_cloud_repo.py` — generate a new cloud repo from selected profile inputs.
- `accb_payload.py` — assemble the `.accb/` payload.
- `accb_inspect.py` — inspect generated payload contents.
- `accb_verify.py` — verify generated repo payload integrity.

## Implemented In PROMPT_17

- `validate_context.py` — validate base context structure.
- `validate_manifests.py` — validate manifest wiring.
- `validate_iac_isolation.py` — validate dev/test IaC isolation.
- `verify_examples.py` — verify canonical examples.
- `run_verification.py` — coordinate verification checks.
- `preview_context_bundle.py` — preview manifest-selected context bundles.
- `pattern_diff.py` — compare generated output against expected patterns.
