# Memory Operating Rules

The memory layer keeps `accb` continuity small and explicit. It separates
tracked architectural truth from local session state so a fresh assistant can
resume work without turning the repository into a transcript.

## Tracked Concepts

- `memory/concepts/` holds durable architectural truths for this base repo.
- Concept files are committed.
- Concept files are updated when architectural truth changes.
- Concept files are not updated for routine implementation details.
- Each concept uses a short heading and a frontmatter-free body.
- Each concept should usually stay between 50 and 150 lines.
- Concept names should be stable, descriptive slugs.
- Concepts should explain why the fact matters to future prompt work.

## Local Session State

- `memory/sessions/` is gitignored session state.
- `memory/summaries/` is gitignored prompt-boundary state.
- These files may be created freely by `scripts/work.py`.
- These files should not be added to `memory/INDEX.md`.
- Local summaries may reference runtime files, but should not duplicate them.
- Local state should be pruned when it stops helping resume work.

## Index Rules

- `memory/INDEX.md` indexes `memory/concepts/` only.
- Do not add entries for `memory/sessions/` files.
- Do not add entries for `memory/summaries/` files.
- Use one-line entries with a short hook.
- Keep the index useful as an orientation map, not a changelog.
- Update the index when a tracked concept is added, renamed, or removed.

## Runtime Continuity

- `context/TASK.md` carries the active boundary and next safe step.
- `context/SESSION.md` carries session-local actions and verification notes.
- `context/MEMORY.md` carries durable repo-local truth for a generated repo.
- These non-example files are local runtime state and are gitignored here.
- Tracked `*.example.md` files define the scaffold copied by `init-project`.
- `scripts/work.py resume` should be the first runtime continuity command after PROMPT_05.

## Update Discipline

- Promote a fact to `memory/concepts/` only when it changes how future work should proceed.
- Keep transient blockers in runtime state, not tracked concepts.
- Prefer exact file paths and exact prompt filenames.
- Remove stale notes instead of accumulating history.
- Checkpoint at prompt boundaries and before handing work to another session.
