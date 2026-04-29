# CLAUDE.md

> **Sync note:** AGENT.md and CLAUDE.md are intentionally near-identical.
> When updating operating rules, update both files. AGENT.md is the source
> of truth for rule wording; CLAUDE.md may add Claude Code-specific notes.

Purpose: boot an assistant into the smallest useful context bundle for this
cloud-native repo (`accb`).

## First Reads

1. `README.md`
2. `docs/repo-layout.md` (after PROMPT_33)
3. `python3 scripts/work.py resume` (after PROMPT_05)
4. `memory/INDEX.md` (after PROMPT_05)
5. `docs/usage/SPEC_DRIVEN_ACCB_PAYLOADS.md` (after PROMPT_33)
6. one router, one workflow, one stack, and one example only when the task
   still needs narrowing

## Operating Rules

- Treat `.accb/` (in derived repos) as the generated repo-local operating
  boundary.
- Treat `tmp/*.md`, `context/TASK.md`, `context/SESSION.md`, and
  `context/MEMORY.md` as local runtime state, not doctrine.
- Validation is mandatory before claiming completion unless the operator
  explicitly waives it. Use `blocked`, `incomplete`, and `done` precisely.
- Always declare the IaC dev/test isolation surface before generating any
  cloud resource: separate state, env-var prefix, secret path, and resource
  naming for `dev` and `test`.
- Prefer manifest-defined bundles over improvised loading.
- Do not add `memory/summaries/` or `memory/sessions/` file entries to
  `memory/INDEX.md`; those directories are gitignored and should only be
  described at the tier level.
- Use `python3 scripts/work.py checkpoint` at natural boundaries (after
  PROMPT_05).

## New Repo Routing

- When started in `agent-cloud-context-base`, assume the operator wants a
  new generated cloud repo unless they explicitly say they want to modify
  the base repo itself.
- For new generated repos, prefer `scripts/new_cloud_repo.py` over manual
  scaffolding (after PROMPT_16).
- Make provider, runtime tier (function | container | k8s), language, IaC
  tool, and dev/test isolation assumptions explicit before generation.

## Claude Code-specific Notes

- Use `Bash`, `Read`, `Edit`, `Write` tools directly; reserve agent spawning
  for genuine multi-step research.
- Treat `tmp/PROMPT_NN_checklist.md` as the per-session todo surface.
- When the user types `/<skill-name>` invoke via the Skill tool only when the
  skill exists in the available list.

## Verification

- Base repo: `python3 scripts/validate_context.py` (after PROMPT_17)
- Generated repo: `python .accb/scripts/accb_verify.py`
- IaC isolation: `python3 scripts/validate_iac_isolation.py <path>`
