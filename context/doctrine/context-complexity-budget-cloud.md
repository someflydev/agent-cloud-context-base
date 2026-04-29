# Context Complexity Budget Cloud

Context size should match task shape. Cloud work becomes expensive when provider, runtime tier, IaC tool, and examples multiply without a specific missing boundary.

## Use Profiles

- Use tiny for a single-file fix.
- Use small for one workflow and one stack.
- Use medium for a workflow plus an adjacent boundary such as function, IaC, and secret binding.
- Use large for multi-role repos such as API, worker, and job together.
- Use cross-cloud only for explicit AWS plus GCP, AWS plus Azure, or similar comparison.

## Apply Penalties

- Add 4 for a secondary provider in one bundle.
- Add 3 for a secondary runtime tier in one bundle.
- Add 4 for Terraform and Pulumi in one bundle unless `comparative_iac_task` is the reason.
- Add 4 for a third example.
- Reduce effective budget by one tier when confidence is below 0.7.

## Escalate With Reason

- Name the missing boundary before loading more context.
- Load a second provider only for explicit comparison or migration.
- Load a second runtime tier only when the task is choosing between tiers.
- Load a second IaC tool only when the task compares tools or migrates between them.
- Reject "for completeness" as an escalation reason.

## Preserve Focus

- Prefer manifests over hand-built bundles.
- Keep examples canonical and provider-specific.
- Keep optional doctrine out of the bundle until triggered.
- Stop when ambiguity would force blended architecture.
- Record unresolved assumptions in the session output.
