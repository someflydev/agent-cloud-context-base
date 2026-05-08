# App Runner public API with VPC Connector

Python service seed for App Runner reaching private Aurora Postgres through
a VPC Connector. The service reads database credentials from AWS Secrets
Manager and deploys from ECR image tag updates.

Dev/test isolation surface:

- State: Terraform `dev` and `test` backends use distinct S3 keys; Pulumi
  stacks are `dev` and `test`.
- Env-var prefix: `ACCB_APPRUNNER_VPC_DEV_` and `ACCB_APPRUNNER_VPC_TEST_`.
- Secret path: `/accb/dev/apprunner/vpc/db` and
  `/accb/test/apprunner/vpc/db`.
- Resource naming: `accb-${environment}-apprunner-vpc-*`.

Lane A runs the service container locally with a `ministack` sidecar for
AWS-compatible test services. Lane B creates isolated real AWS test resources
and must be destroyed immediately. Expected Lane B cost band: medium,
bounded by App Runner, VPC connector, ECR, Secrets Manager, and small Aurora
test resources.
