# Router System

PROMPT_06 established the accb router system: task, provider, runtime tier, stack, archetype, scenario, and IaC decisions stay independent until manifests and payload composition combine them into the smallest useful context bundle. Provider, runtime, and IaC ambiguity are explicit stop conditions; cross-cutting support such as secrets, eventing, storage, identity, and observability is loaded only when the task activates it. The machine-checkable route-check feature gate remains off by default in `context/accb/profile-rules.json` and is implemented through `scripts/work.py`.
