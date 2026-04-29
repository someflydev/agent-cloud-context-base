# Manifest Selection

Use this skill to choose between near-match manifests for an `accb` workload without merging them or widening the context bundle as a hedge. It resolves ambiguity by scoring repo and prompt signals, preferring narrower scope on ties, and stopping when no manifest clearly dominates.

## Procedure

1. List candidate manifests that match provider, runtime tier, language, IaC tool, archetype, and support-service signals.
2. Read `context/router/repo-signal-hints.json` when present because it is the machine-readable signal guide.
3. Treat lockfiles, IaC files, framework entrypoints, import families, and existing manifest references as strong signals.
4. Treat one-off comments, documentation mentions, speculative examples, or user brainstorming as weak signals.
5. Score each candidate by the number and quality of matching signals.
6. Reject candidates that contradict explicit provider, runtime tier, language, IaC, or dev/test isolation choices.
7. When scores tie, prefer the manifest with the narrower scope and fewer optional context items.
8. Do not combine two near-match manifests unless the task is explicitly comparative.
9. Stop and name the ambiguity when no manifest dominates after scoring.
10. Record the selected manifest and the decisive signals in the bundle assembly notes.

## Good Triggers

- "which manifest should I use?"
- "two manifests look close"
- "manifest tie"
- "repo signals are mixed"
- "pick the profile"
- "narrower manifest or broader manifest?"

## Avoid

- choosing the manifest that loads the most context as insurance
- merging manifests for a normal single-provider task
- ignoring strong repo signals in favor of a weak prompt aside
- selecting a manifest that contradicts newer doctrine
- proceeding silently when the ambiguity remains unresolved
