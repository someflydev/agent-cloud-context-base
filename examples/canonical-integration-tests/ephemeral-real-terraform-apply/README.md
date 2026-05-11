# Ephemeral Real Terraform Apply

Lane: real cloud (Lane B). Approximate runtime: 5-15 minutes. Approximate cost:
real cloud charges may apply.

This harness applies a minimal `test` workspace with `terraform
apply -auto-approve`, runs pytest assertions, and destroys the workspace. It is
skipped unless `ACCB_RUN_REAL_CLOUD=1`, provider credentials, and
`ACCB_TERRAFORM_DIR` are available. Keep `ACCB_MAX_REAL_CLOUD_SECONDS` low for
CI.
