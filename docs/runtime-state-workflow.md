# Runtime State Workflow

`accb` separates durable doctrine from local runtime state. Runtime files explain the current operator session; they do not override manifests, specs, or validation gates.

| State surface | Role | Transition command |
| --- | --- | --- |
| `PLAN.md` | Optional roadmap for multi-step work in the base repo or a generated repo | Create or revise directly, then `python3 scripts/work.py checkpoint` |
| `context/TASK.md` | Current task brief copied from `context/TASK.example.md` | `python3 scripts/work.py init-project` then edit the active task |
| `context/SESSION.md` | Current session notes, assumptions, and proof commands | `python3 scripts/work.py resume`, `checkpoint`, `pause`, `done` |
| `context/MEMORY.md` | Local high-signal continuity notes for the active repo | `python3 scripts/work.py checkpoint` after meaningful changes |
| `memory/summaries/` | Gitignored per-prompt summaries | `python3 scripts/work.py checkpoint` and `done` |
| `memory/sessions/` | Gitignored session logs | `python3 scripts/work.py start`, `pause`, `done` |

## Command Pairings

| Transition | Command | Expected use |
| --- | --- | --- |
| Initialize runtime files | `python3 scripts/work.py init-project` | Copy tracked examples into active runtime files. |
| Resume work | `python3 scripts/work.py resume` | Print git anchor, changed files, runtime file status, and next-step hints. |
| Record a boundary | `python3 scripts/work.py checkpoint` | Capture a natural pause after a doc, generation, or validation slice. |
| Pause | `python3 scripts/work.py pause --reason "<reason>"` | Stop with a reason when validation or operator input blocks progress. |
| Complete | `python3 scripts/work.py done --summary "<summary>"` | Mark completion only after validation proof exists. |
| Select next prompt | `python3 scripts/work.py next` | Continue the prompt-first build sequence. |

Use `blocked`, `incomplete`, and `done` precisely: `done` means proof was run and the result is known.
