# Session Start

## In `accb` Itself

1. Read [`AGENT.md`](../AGENT.md).
2. Run `python3 scripts/work.py resume`.
3. Read [`docs/repo-layout.md`](repo-layout.md) if the task needs repo shape.
4. For generation tasks, declare provider, runtime tier, language, IaC tool, and dev/test isolation before running `scripts/new_cloud_repo.py`.
5. Validate with the narrowest relevant command, then broaden to `python3 scripts/work.py verify` before claiming `done`.

Useful commands:

```bash
python3 scripts/work.py resume
python3 scripts/new_cloud_repo.py --help
python3 scripts/run_verification.py --tier fast
python3 scripts/work.py verify
```

## In a Generated Repo

1. Read `AGENT.md` or `CLAUDE.md` in the generated repo.
2. Read `.accb/SESSION_BOOT.md`.
3. Inspect `.accb/profile/selection.json` for provider, runtime tier, language, IaC tool, manifest, support services, and scenario patterns.
4. Run `python3 scripts/work.py resume` if the generated repo includes the continuity script.
5. Run `python3 .accb/scripts/accb_verify.py` before making cloud changes.

Useful commands:

```bash
python3 scripts/work.py resume
python3 .accb/scripts/accb_verify.py
python3 .accb/scripts/accb_inspect.py
```
