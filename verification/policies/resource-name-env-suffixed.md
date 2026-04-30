# Resource Name Env Suffixed

Cloud resource names must include a deterministic environment component such as
dev or test.

The failure mode is a cross-environment name collision. Buckets, queues, topics,
functions, clusters, identities, and databases often have provider-wide or
project-wide naming constraints, so one environment can block or mutate another.

Use a shared naming helper or IaC variable based on the environment. For Pulumi,
derive names from the current stack. For Terraform, derive names from an
environment variable or local.

When this policy fails, introduce a naming helper and update every declared
resource that can be externally addressed.
