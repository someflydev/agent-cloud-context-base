# Prompt First Conventions

The prompt sequence is the construction ledger for `accb`. Each prompt must be self-contained enough for a fresh assistant session to continue the arc without relying on unstated memory.

## Number Prompts Monotonically

- Store prompts in `.prompts/PROMPT_NN.txt`.
- Never renumber existing prompts.
- Never reuse a skipped number.
- Treat each prompt as one bounded session of work.
- Stop at the declared prompt boundary.

## Make Prompts Self Contained

- Embed the shared context briefing needed for the session.
- Declare the exact boot sequence.
- List the files and directories in scope.
- Name verification commands before completion gates.
- Explain follow-up boundaries for later prompts.

## Track Session State

- Use `tmp/PROMPT_NN_checklist.md` for per-session checklist state.
- Keep `tmp/` state local and gitignored.
- Use `memory/summaries/PROMPT_NN_*.md` for resume and completion summaries once runtime support exists.
- Keep summaries out of `memory/INDEX.md`.
- Use `context/TASK.md`, `context/SESSION.md`, and `context/MEMORY.md` as runtime state after PROMPT_05.

## Preserve Runtime Discipline

- Let `scripts/work.py` manage queue, quota, pause, resume, start, and done state after it exists.
- Checkpoint at natural boundaries after PROMPT_05.
- Keep a prompt's verification tied to the files it changed.
- Use `done`, `blocked`, and `incomplete` precisely.
- Do not claim a prompt complete without its proof path.

## Keep Naming Consistent

- Use `accb` for this base repository.
- Use `.accb/` for derived repo payloads.
- Avoid legacy shorthand from other context bases.
- Keep prompt language cloud-native.
- Keep examples aligned to AWS, GCP, Azure, Terraform, Pulumi, functions, containers, and Kubernetes.
