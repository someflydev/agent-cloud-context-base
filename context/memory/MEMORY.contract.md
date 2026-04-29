# MEMORY.md Contract

`context/MEMORY.md` is the generated repo's durable repo-local continuity
file. It records stable truths that a future assistant should know before
loading stack detail.

It is not a transcript, task checklist, doctrine file, or replacement for
manifests. It changes at prompt boundaries and when architectural truth changes.
It does not change after every command.

Limits:

- maximum 300 lines
- maximum 3000 words
- frontmatter-free Markdown
- exact file paths when paths matter
- concise bullets preferred over narrative

## Required Sections

### Repo Purpose

State what the generated cloud repo is for. Include provider, runtime tier,
language, and IaC tool when known.

### Active Boundary

State the current architectural or prompt boundary. This may be the selected
archetype, manifest, workflow, or cloud integration surface.

### Non-obvious Invariants

Record constraints that future sessions must preserve. For cloud repos this
often includes trigger contracts, identity boundaries, dev/test isolation,
managed-service assumptions, naming rules, and replay behavior.

### Known Gotchas

Record facts that would otherwise cause repeated rediscovery. Keep this to
real pitfalls, not ordinary implementation notes.

### External References

List external docs, dashboards, provider resources, tickets, or runbooks that
matter to the repo. Do not include secret values.

## Update Rules

Update `context/MEMORY.md` when:

- the repo purpose becomes clearer
- provider, runtime tier, language, or IaC selection changes
- dev/test isolation truth changes
- a non-obvious invariant is discovered
- a known gotcha materially affects future work
- a prompt boundary finishes and continuity truth changed

Do not update it for:

- routine command output
- transient next steps
- every edited file
- copied doctrine
- secrets or credential material
