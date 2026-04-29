# Stop Conditions

Stopping is a correctness tool. When a cloud decision would change architecture, cost, identity, or environment isolation, do not improvise a blended pattern.

## Stop For Provider Ambiguity

- Stop when more than one provider is plausible and the task is not comparative.
- Name the plausible providers.
- Ask for the smallest missing decision or use a declared repo signal.
- Do not mix AWS, GCP, and Azure defaults.
- Do not load multiple provider stack packs to compensate.

## Stop For Runtime Ambiguity

- Stop when function, managed container, and Kubernetes are all plausible.
- Name the trigger, duration, topology, or scaling fact that would decide the tier.
- Do not generate a function and container version in parallel.
- Do not choose Kubernetes without a topology reason.
- Re-enter routing after the tier is known.

## Stop For IaC Ambiguity

- Stop when Terraform and Pulumi are both plausible.
- Stop when Pulumi language is unknown and no repo signal decides it.
- Do not produce both Terraform and Pulumi for one non-comparative task.
- Do not share state assumptions across tools.
- Require dev/test state, secret, and naming isolation before resource generation.

## Stop For Boundary Gaps

- Stop when a managed-service substitute has no provider-native equivalent and BYO is not justified.
- Stop when dev/test isolation surface is undefined.
- Stop when secret ownership is unclear.
- Stop when event replay behavior is undefined for an event-driven task.
- Name the ambiguity and the smallest missing decision.
