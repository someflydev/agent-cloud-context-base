# No Checked In Tfvars Or Pulumi Secrets

Do not commit `terraform.tfvars` or encrypted Pulumi config files to example or
generated repositories.

The failure mode is source-controlled environment state. Even encrypted config
can couple examples to one operator, one backend, or one key-management setup.
Plain Terraform variable files frequently carry account identifiers or secrets.

Commit example variable templates instead, such as `terraform.tfvars.example`,
and document how the operator supplies real values outside git.

When this policy fails, move the real config out of the repository and add an
example file with safe placeholder values.
