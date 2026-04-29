# Context Loading Rules

Cloud tasks should load the smallest bundle that can decide and execute the work. Context is added by routing signal, not by scanning the repository for reassurance.

## Route First

- Infer provider, runtime tier, language, IaC tool, and environment from the request and repo signals.
- Load one router before loading stack detail.
- Use the router to choose the workflow and bundle.
- Stop when more than one primary provider remains plausible.
- Stop when more than one primary runtime tier remains plausible.

## Load One Primary Bundle

- Load one workflow.
- Load one provider, runtime, and language stack pack.
- Load one archetype.
- Load one canonical example.
- Load optional context only when the task activates it.

## Treat IaC As Adjacent

- Add one IaC stack when the task touches cloud resources.
- Do not count the IaC stack against the runtime stack cap.
- Choose Terraform or one Pulumi language, not both, unless the task is comparative.
- Include dev/test isolation doctrine with IaC changes.
- Use manifests to assemble the bundle.

## Avoid Broad Scans

- Do not load multi-provider context unless the task explicitly compares providers.
- Do not scan all of `context/`, `examples/`, or `manifests/`.
- Do not load a second example for completeness.
- Escalate context only by naming the missing boundary.
- Mark uncertainty instead of blending patterns.
