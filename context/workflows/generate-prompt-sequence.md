# Generate Prompt Sequence

Use this workflow when authoring `.prompts/PROMPT_NN.txt` files for a derived cloud repo so future sessions can advance the repo in small, verifiable, commit-friendly increments.

## Preconditions

- The current repo state has been inspected, including existing `.prompts/`, `.accb/`, tests, IaC, and runtime files.
- The target end state is concrete enough to decompose into ordered changes.
- Any cloud resource work includes a declared dev/test isolation surface.

## Sequence

1. Identify the end state in terms of files, cloud boundaries, tests, and validation commands.
2. Inventory the actual current files and avoid references to future files unless the prompt creates them.
3. Split the work into monotonic prompt numbers that each end at a commit-friendly checkpoint.
4. Put generation, runtime implementation, IaC, tests, docs, and validation in the smallest order that keeps each prompt runnable.
5. Reference exact paths and expected commands in every prompt.
6. Include stop conditions when provider, runtime tier, or isolation assumptions conflict.
7. Require verification before completion and name `blocked`, `incomplete`, or `done` precisely.
8. Add resume notes or memory updates only when the repo's durable context changes.

## Outputs

- `.prompts/PROMPT_NN.txt` files with ordered, executable work.
- A prompt sequence that references actual repo state at every step.

## Validation Gates

- `startup-rehydration` from `profile-rules.json`
- `changed-boundary-proof`

## Related Docs

- `context/doctrine/prompt-first-conventions.md`
- `context/doctrine/context-complexity-budget-cloud.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Writing prompts that assume files from later prompts already exist.
- Bundling too many cloud boundaries into one prompt.
- Omitting validation commands because the prompt only edits documentation.
