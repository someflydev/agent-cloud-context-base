# Memory Continuity Discipline

Use this skill to decide what belongs in `MEMORY.md`, a concept artifact, summaries, or live task/session files. It resolves ambiguity by separating durable architectural truths from prompt completion notes and local runtime state.

## Procedure

1. Classify the information by lifespan before writing it.
2. Put durable architectural truths, doctrine summaries, and reusable system facts in `memory/concepts/`.
3. Put durable facts that must be discovered quickly in `memory/INDEX.md` as links to tracked concept artifacts.
4. Put per-prompt resume and completion notes in `memory/summaries/`.
5. Put active per-session checklists in `tmp/`.
6. Put local live state in `context/TASK.md`, `context/SESSION.md`, or `context/MEMORY.md` only when the current derived repo needs it.
7. Do not add individual `memory/summaries/` or `memory/sessions/` files to `memory/INDEX.md`.
8. Prune stale operational state instead of promoting it to durable memory.
9. At prompt completion, write the smallest concept note that helps future prompts avoid rediscovery.
10. Run `python3 scripts/work.py checkpoint` at natural boundaries after PROMPT_05 when available.

## Good Triggers

- "where should this memory go?"
- "update MEMORY.md"
- "write a concept artifact"
- "prompt completion summary"
- "memory index"
- "session checklist"

## Avoid

- storing transient checklist state in durable concepts
- treating `context/MEMORY.md` as doctrine
- indexing gitignored summary or session files individually
- duplicating implementation details already present in code
- keeping stale resume notes as authoritative after completion
