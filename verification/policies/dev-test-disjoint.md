# Dev Test Disjoint

Dev and test infrastructure must have separate state keys, names, secret paths,
and identity bindings.

The failure mode is cross-environment mutation: a test run can update dev state,
reuse a dev secret, or collide with an existing resource name. That makes cleanup
dangerous and makes validation results untrustworthy.

Terraform backends may share backend infrastructure, but the per-environment key
or prefix must differ. Pulumi stacks must use distinct stack names and backend
paths when backend config is present.

When this policy fails, split the state path, add deterministic environment
suffixes, and use separate secret paths before generating resources.
