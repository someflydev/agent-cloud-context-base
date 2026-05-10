# Scripts

`scripts/` holds repo-local automation for `accb`.

## Runtime Continuity

`work.py` manages local runtime state, checkpointing, startup inspection, and
graft support.

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

## Generation And Payloads

- `new_cloud_repo.py` - generate a new cloud repo from selected profile inputs
  and starter templates.
- `accb_payload.py` - assemble the generated repo `.accb/` payload.
- `accb_inspect.py` - inspect generated payload contents.
- `accb_verify.py` - verify generated repo payload integrity.

## Validation And Drift Checks

- `validate_context.py` - validate base context structure.
- `validate_manifests.py` - validate manifest wiring.
- `validate_iac_isolation.py` - validate dev/test IaC isolation.
- `verify_examples.py` - verify canonical examples.
- `run_verification.py` - coordinate verification tiers.
- `preview_context_bundle.py` - preview manifest-selected context bundles.
- `pattern_diff.py` - compare generated output against expected patterns.
- `render_parity_matrix.py` - render the provider parity documentation.

## Common Commands

```bash
python3 scripts/work.py resume
python3 scripts/new_cloud_repo.py --help
python3 scripts/accb_payload.py --help
python3 scripts/validate_context.py
python3 scripts/validate_manifests.py
python3 scripts/run_verification.py --tier fast
```
