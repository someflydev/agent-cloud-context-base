# K8s Workload Role Decomposition

Use this skill to split a proposed Kubernetes workload into API, worker, job, cron, and control-plane roles. It resolves ambiguity by separating runtime classes so each role can scale, deploy, recover, and communicate according to its lifecycle instead of being packed into one deployment.

## Procedure

1. List every behavior the prompt requests, including request handling, background work, batch work, scheduled work, and reconciliation.
2. Classify each behavior by latency, scaling signal, lifecycle, resource class, and rollout risk.
3. Put synchronous user-facing traffic into API Deployments.
4. Put queue or stream consumers into worker Deployments with independent scaling.
5. Put bounded one-off processing into Jobs.
6. Put scheduled work into CronJobs with explicit concurrency policy and missed-run behavior.
7. Put reconciliation or platform ownership into a control-plane Deployment only when it manages durable desired state.
8. Document cross-piece communication through service calls, queues, topics, streams, or shared stores.
9. Define identity, secrets, network policy, probes, resource requests, and observability per role.
10. Stop when the proposed roles imply different runtime tiers and runtime routing has not been resolved.

## Good Triggers

- "split this k8s workload"
- "API plus workers plus jobs"
- "multi-role platform"
- "cronjob or worker?"
- "control plane workload"
- "separate scaling and recovery"

## Avoid

- running API, worker, and cron behavior in one Deployment by default
- using Kubernetes when a managed container with one worker would satisfy the topology
- hiding role communication in shared database polling without cause
- giving all roles the same identity and secret access
- omitting probes and resource requests for long-running roles
