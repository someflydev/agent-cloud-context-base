# Function Vs Container Vs K8s

Runtime tier selection should follow workload shape, not preference. Start one tier lower when the fit is uncertain, then escalate only when limits, binaries, traffic, topology, or isolation make the next tier necessary.

## Choose Function

- Use a function for one trigger, one short transformation, and one persistence step.
- Stay within provider time, memory, payload, and package limits.
- Accept cold-start behavior as compatible with the user-facing contract.
- Prefer functions for S3, Pub/Sub, Event Grid, queue, webhook, and scheduler edges.
- Keep orchestration outside the handler when a workflow service is available.

## Choose Managed Container

- Use Cloud Run, App Runner, or Container Apps when custom binaries are required.
- Choose a managed container when request duration or startup behavior exceeds function fit.
- Use a managed container for steady traffic where cold starts hurt.
- Keep a small companion set such as a private worker or scheduled job in the same tier.
- Stay in the managed container tier until multiple workload classes need independent platform control.

## Choose Kubernetes

- Use Kubernetes when topology is structural.
- Choose EKS, GKE, or AKS for API, worker fleet, jobs, crons, and controller workloads that scale separately.
- Use Kubernetes when workload recovery, rollout, service mesh, or namespace isolation is central.
- Account for cluster, node, add-on, image, and security operations before committing.
- Pay the Kubernetes cost only when its topology solves a real problem.

## Escalate With Evidence

- Name the limit or operational requirement that breaks the current tier.
- Preserve the external contract while changing the runtime tier.
- Update IaC, identity, observability, and tests with the new boundary.
- Avoid moving to Kubernetes only for familiarity or future possibility.
- Prefer a managed container before Kubernetes when one service and one worker are enough.

## Keep Tier Decisions Visible

- Record the selected tier in the manifest.
- Pair the tier with provider, language, IaC tool, and dev/test isolation assumptions.
- Route to canonical examples for the selected cell.
- Say when no verified example exists.
- Revisit the tier when traffic, runtime limits, or topology changes.
