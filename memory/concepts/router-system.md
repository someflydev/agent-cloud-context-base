# Router System

PROMPT_06 establishes the accb router system: task, provider, runtime tier, stack, archetype, scenario, and IaC decisions are kept independent until a later bundle assembler combines them into the smallest useful context bundle. Provider, runtime, and IaC ambiguity are explicit stop conditions; cross-cutting support such as secrets, eventing, storage, identity, and observability is loaded only when the task activates it. The machine-checkable route-check feature gate remains off in `context/accb/profile-rules.json` until PROMPT_17 wires the route-check engine.
