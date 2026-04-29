# Stop Hook Guidance

When a hook, quota trigger, missing prerequisite, or operator instruction
requires stopping mid-session, leave the repo in a state that a fresh assistant
can resume without guessing.

## Required Stop Steps

1. Write `tmp/HANDOFF.md`.
2. Include the exact resume command in `tmp/HANDOFF.md`.
3. Write `memory/summaries/PROMPT_NN_resume.md`.
4. Run `python3 scripts/work.py checkpoint`.
5. State the blocker explicitly in `context/TASK.md` as `Blocked by: ...`.

## Resume Command

The resume command should be complete enough to paste into a new session. For
this base repo, use:

```sh
Load AGENT.md, then run .prompts/PROMPT_NN.txt
```

For a generated repo with an `.accb/` layer, use the repo-local startup command
documented by that payload.

## Blocker Notes

Blockers should name the missing condition, not just the symptom.

Useful blocker notes include:

- missing cloud credentials
- unavailable quota
- prompt boundary reached
- validation command missing until a later prompt
- operator decision required

Do not mark a stopped prompt as `done` unless its verification contract has
actually passed.
