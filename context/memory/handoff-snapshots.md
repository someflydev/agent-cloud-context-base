# Handoff Snapshots

Handoff snapshots are local prompt-boundary files under
`memory/summaries/`. They preserve the state needed by the next session
without committing session notes.

## Resume Snapshot

Write `memory/summaries/PROMPT_NN_resume.md` when a prompt pauses before it
is complete.

It should capture:

- the boundary reached
- what is safe to pick up next
- the files most likely to matter
- verification already run
- blockers or missing prerequisites
- the full command the next session should run

The resume snapshot should not duplicate `context/TASK.md`, `context/SESSION.md`,
or `context/MEMORY.md`. Point to those files when they already hold the current
state.

## Completion Snapshot

Write `memory/summaries/PROMPT_NN_completion.md` when a prompt completes and
future sessions may need proof of the outcome.

It should capture:

- what the prompt delivered
- what verification passed
- what verification was blocked or deferred
- any follow-up prompt boundary already known
- runtime-state files updated at the boundary

## Storage Rules

- Resume and completion snapshots are gitignored.
- They survive across local sessions through `scripts/work.py` conventions.
- They are not indexed in `memory/INDEX.md`.
- They should stay short enough to read during startup.
- They should use exact prompt filenames such as `.prompts/PROMPT_05.txt`.
