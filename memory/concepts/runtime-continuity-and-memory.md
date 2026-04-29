# Runtime Continuity And Memory

PROMPT_05 adds the first runtime continuity layer to `accb`. Before this
point, the repository relied on static doctrine, anchors, specs, validation
narratives, and the prompt sequence itself. After this point, sessions have a
standard local tool for resuming, checkpointing, and recording prompt-state
transitions.

The runtime tool is `scripts/work.py`. It is intentionally stdlib-only so it
can run in a fresh clone without dependency installation. The tool handles
startup inspection, prompt status rows, quota notes, lightweight checkpoints,
and later grafting of a minimal `.accb/` continuity layer into generated or
existing repos.

The key startup command is:

```sh
python3 scripts/work.py resume
```

The command prints a Session Context Briefing with the current git anchor,
runtime-file state, next-step hint, plan review signal, complexity posture,
quota readiness, and any relevant prompt summary. The briefing is a routing
aid, not a substitute for reading the files named by the active boundary.

Runtime files are deliberately split:

- `PLAN.md` is local roadmap state.
- `context/TASK.md` is the active boundary and next safe step.
- `context/SESSION.md` is the session action and verification note.
- `context/MEMORY.md` is durable repo-local truth for generated repos.

The non-example versions are gitignored. The tracked `*.example.md` files
define the scaffold copied by `python3 scripts/work.py init-project`.

The tracked memory tier is `memory/concepts/`. These files hold durable
architectural truth for the base repo and are indexed by `memory/INDEX.md`.
They should be updated only when a fact changes how future sessions should
work.

The local memory tiers are `memory/sessions/` and `memory/summaries/`.
They are gitignored and should not receive index entries. Summary files are
used at prompt boundaries, especially `PROMPT_NN_resume.md` and
`PROMPT_NN_completion.md`.

`context/memory/` defines the operating contract for generated repos and for
future grafted `.accb/` payloads. It includes rules for memory operation,
handoff snapshots, stop-hook behavior, and the `context/MEMORY.md` schema.

PROMPT_05 also establishes feature gates for startup helpers. The
`budget-report`, `route-check`, and `startup-trace` subcommands consult
`context/accb/profile-rules.json`. In the current base profile those features
are gated off, so the commands exit successfully with a clear gated message.

The checkpoint command does not rewrite runtime files automatically. It writes
only `work/checkpoint.log` and reminds the operator to review TASK, SESSION,
and MEMORY when the active boundary changed. This keeps runtime continuity
explicit instead of silently mutating local state.

The graft command is intentionally narrow. It installs only the minimal
runtime continuity layer under `.accb/`: the work tool, memory operating
rules, and the prompt-first analysis template when that template exists after
PROMPT_15. It must not copy doctrine, archetypes, stacks, examples, or
validation content into the target repo.

This milestone means future prompt sessions should start with `AGENT.md`,
then `python3 scripts/work.py resume`, then the smallest prompt-specific
bundle needed for the active task.
