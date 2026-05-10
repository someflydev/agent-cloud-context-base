# Verification Policies

Static lint policies enforced by validate_iac_isolation and run_verification.

Each policy has a short Markdown explanation plus a matching
`*.policy.yaml` fixture where the rule is machine-readable. Current policies
cover:

- dev/test resource disjointness
- no default credentials
- no checked-in tfvars or Pulumi secrets
- environment-suffixed resource names
- secrets not committed in source
