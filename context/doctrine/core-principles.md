# Core Principles

Cloud context should make the smallest useful backend easy to build, verify, and operate. Prefer a clear v1 that proves the workload boundary over a speculative platform that hides risk behind abstractions.

## Start Small

- Build the smallest cloud surface that satisfies the operator's request.
- Prefer one function, one managed container, or one workload class before adding a platform.
- Escalate only when trigger shape, runtime limits, scaling topology, or compliance requires it.
- Treat v1 as a working proof path, not a placeholder for an imagined v3.
- Keep generated repositories lean until real implementation earns more structure.

## Keep Layers Separate

- Use doctrine for durable rules and reasoning.
- Use workflows for ordered task execution.
- Use stacks for provider, runtime, language, and IaC implementation guidance.
- Use archetypes for product-shaped bundles.
- Use examples for verified runnable patterns.
- Use templates for scaffolding only.
- Use skills for assistant procedures.
- Use anchors for compact reminders.
- Use specs and validation for machine-checkable contracts.

## Infer From User Intent

- Translate user requests into cloud terms without forcing internal vocabulary on them.
- Route "add an S3-triggered Lambda" to the smallest relevant bundle.
- Name assumptions when provider, runtime tier, language, IaC tool, or isolation mode is missing.
- Prefer practical cloud artifacts over taxonomy talk in generated output.
- Surface uncertainty before it changes architecture.

## Prefer Canonical Patterns

- Choose the verified pattern for a provider, runtime tier, language, and IaC cell.
- Avoid hybrid designs that mix platforms without a stated operational reason.
- Keep AWS Lambda, Cloud Run, Azure Container Apps, EKS, GKE, and AKS patterns recognizable.
- Audit examples when a doctrine rule changes.
- Say when no canonical example exists instead of improvising silently.

## Prove Boundaries

- Test functions at the trigger and managed-service boundary.
- Test containers through health, request, and background-worker contracts.
- Test Kubernetes workloads through readiness, service routing, job, and controller behavior.
- Declare dev and test isolation before creating cloud resources.
- Treat `done` as a proven state; use `blocked` or `incomplete` when proof is missing.

## Keep The Base Focused

- Treat `accb` as a foundation for generated repositories, not a permanent meta-platform.
- Document the base repo fully because documentation is its product.
- Defer front-facing docs in derived repos until implementation has real behavior.
- Keep prompt sequence work bounded to the current prompt.
- Preserve `.accb/` as the generated repo payload boundary.
