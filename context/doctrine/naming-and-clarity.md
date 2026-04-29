# Naming And Clarity

Cloud names should make environment, repo, and role visible. Clear names reduce teardown risk, audit confusion, and accidental cross-environment access.

## Use Predictable Shape

- Use `<repo>-<env>-<role>` for resource names.
- Use names such as `intake-dev-api` and `intake-test-worker`.
- Include the trigger in function names such as `intake-test-on-s3-put`.
- Use the same environment suffix across buckets, queues, topics, services, and identities.
- Keep names deterministic enough for scripts and validation.

## Separate User Names From IaC Shorthand

- Avoid abbreviations such as `sg`, `vpc`, or `rg` in user-facing names.
- Allow provider shorthand inside IaC when context is unambiguous.
- Prefer `security_group_id` over unclear output names.
- Use snake_case for IaC outputs.
- Type module variables explicitly.

## Make Environment Obvious

- Never reuse dev names for test.
- Include environment in secret paths.
- Include environment in state backend keys or stack names.
- Include environment in log groups, metrics, and dashboards.
- Include environment in test fixture resources.

## Favor Auditability

- Name roles by what they do, not by implementation detail.
- Keep names short enough for provider limits.
- Document unavoidable truncation rules.
- Avoid random suffixes unless provider uniqueness requires them.
- Preserve a stable prefix so resources remain searchable.
