# Ephemeral Real Pulumi Up/Down

Lane: real cloud (Lane B). Approximate runtime: 5-15 minutes. Approximate cost:
real cloud charges may apply.

This harness intentionally creates cloud resources in a minimal `test` stack
through the Pulumi CLI, reads stack outputs, and destroys the stack. It is
skipped unless `ACCB_RUN_REAL_CLOUD=1`, provider credentials, and
`ACCB_PULUMI_WORK_DIR` are available. Keep `ACCB_MAX_REAL_CLOUD_SECONDS` low
for CI.
