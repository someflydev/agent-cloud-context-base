# AGENT.md

Purpose: boot an assistant into the smallest useful context bundle for
`{{repo_name}}`, a {{archetype}} repo generated with accb.

## Profile

- Archetype: `{{archetype}}`
- Provider: `{{provider}}`
- Runtime tier: `{{runtime_tier}}`
- Primary language: `{{primary_language}}`
- IaC tool: `{{iac_tool}}`

## First Reads

1. `README.md`
2. `.accb/profile/selection.json`
3. `python3 scripts/work.py resume`
4. `.accb/context/MEMORY.md` when present
5. one stack or workflow document only when the task needs narrowing

## Operating Rules

- Treat `.accb/` as the generated repo-local operating boundary.
- Treat `tmp/*.md`, `context/TASK.md`, `context/SESSION.md`, and
  `context/MEMORY.md` as runtime state, not doctrine.
- Validation is mandatory before claiming completion unless the operator
  explicitly waives it. Use `blocked`, `incomplete`, and `done` precisely.
- Declare the IaC dev/test isolation surface before generating cloud
  resources: state, env-var prefix, secret path, and resource naming.
- Dev isolation: `{{state_backend_dev}}`, `{{env_var_prefix_dev}}`,
  `{{secret_path_dev}}`, `<{{repo_slug}}>-dev-<role>`.
- Test isolation: `{{state_backend_test}}`, `{{env_var_prefix_test}}`,
  `{{secret_path_test}}`, `<{{repo_slug}}>-test-<role>`.
- Prefer manifest-defined bundles over improvised loading.

## New Repo Routing

- This repo has already been generated from accb; modify the local repo
  unless the operator explicitly asks to regenerate from the base.
- Keep provider, runtime tier, language, IaC tool, and dev/test isolation
  assumptions explicit before adding resources.

## Verification

- Generated repo: `python .accb/scripts/accb_verify.py`
- IaC isolation: `python .accb/scripts/validate_iac_isolation.py .`
