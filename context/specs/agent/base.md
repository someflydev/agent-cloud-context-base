---
accb_origin: canonical
accb_source_path: context/specs/agent/base.md
accb_role: agent
accb_version: 1
---

# Baseline Agent Operating Rules

Agents act autonomously only inside explicit constraints. The default rhythm is
to rehydrate local context, identify one active boundary, plan the validation
path before coding, implement one reviewable slice, run the relevant checks,
and update continuity artifacts only when the truth changed.

At session start, re-read `.accb/SESSION_BOOT.md` and
`.accb/profile/selection.json`. Before loading stack packs, declare provider,
runtime tier, language, and IaC tool. Before generating cloud resources,
declare the dev/test isolation surface: separate state, env-var prefix, secret
path, and resource naming.

Do not claim completion until the relevant checks actually ran. If proof is
blocked by missing credentials, quota, cloud access, or an unavailable harness,
say `blocked`. If work remains or the proof path has not run, say
`incomplete`. Say `done` only after the proof ran and the observed result
matches the validation contract.
