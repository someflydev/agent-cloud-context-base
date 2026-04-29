# Cloud Runtime Tier Selection

Use this skill to choose between function, managed-container, and k8s when a workload could plausibly fit more than one runtime tier. It resolves ambiguity by starting from workload boundedness and escalating only when limits, binaries, topology, scaling, or isolation make a lower tier insufficient.

## Procedure

1. Identify the boundedness of the workload: one trigger and short effect, one service with companions, or multiple independent workload classes.
2. Confirm runtime needs: duration, memory, payload size, package size, startup behavior, and custom binary requirements.
3. Map topology: single handler, API plus worker or job, or API, workers, jobs, crons, and control-plane roles.
4. Name scaling axes: request concurrency, queue depth, scheduled work, tenant isolation, CPU or GPU class, and rollout independence.
5. Choose the lowest runtime tier that satisfies the stated contract.
6. Select `function` for short trigger-driven work with provider limits and cold starts accepted.
7. Select `managed-container` when custom binaries, steady traffic, longer request duration, or a small companion set break function fit.
8. Select `k8s` when separate workload roles, namespace isolation, mesh policy, KEDA-style scaling, or platform control are structural.
9. Document the escalation trigger in plain language, including what lower tier failed.
10. Record the selected tier with provider, language, IaC tool, and dev/test isolation assumptions before generating resources.

## Good Triggers

- "function or container?"
- "should this be Kubernetes?"
- "what runtime tier fits this workload?"
- "Cloud Run or Cloud Functions?"
- "Lambda, App Runner, or EKS?"
- "the prompt could be serverless or k8s"

## Avoid

- escalating to Kubernetes for familiarity or future possibility
- choosing a function when custom binaries or long-running work dominate
- choosing a managed container without naming the function limit that failed
- ignoring cold-start impact on user-facing paths
- treating runtime tier as independent from identity, observability, IaC, and tests
