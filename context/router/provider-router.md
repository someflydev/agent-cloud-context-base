# Provider Router

The provider router decides whether the active cloud provider is AWS, GCP, or Azure by reading prompt language and repo signals. It does not decide runtime tier, language, IaC tool, workload topology, or whether a managed service is appropriate beyond identifying which provider family owns the signal.

## Core Rule

Choose exactly one provider for non-comparative work only when user language or repo signals make that provider dominant.

## Mappings / Signals

- "lambda", "s3", "dynamodb", "eventbridge", "sqs", "sns", "iam role", "rds", "cloudwatch", "ses", "sagemaker", "cognito", "step functions", "amazon"
  - provider `aws`
- `terraform/aws/`, `pulumi-aws-*`, `lambda_function.py`, `provider "aws"`, `serverless.yml`
  - provider `aws`
- imports containing `boto3`, `@aws-sdk/`, `aws-sdk-go`, or `Amazon.`
  - provider `aws`
- "cloud function", "gcs", "firestore", "pub/sub", "cloud run", "bigquery", "vertex ai", "cloud sql", "cloud scheduler", "eventarc", "service account"
  - provider `gcp`
- `terraform/gcp/`, `pulumi-gcp-*`, Functions Framework decorators
  - provider `gcp`
- imports containing `google.cloud`, `@google-cloud/`, or `cloud.google.com/go`
  - provider `gcp`
- "azure function", "blob", "cosmos", "service bus", "event grid", "event hubs", "key vault", "azure sql", "azure openai", "managed identity", "azure ai search"
  - provider `azure`
- `terraform/azurerm/`, `pulumi-azure-*`, `host.json`, `function.json`, `local.settings.json`
  - provider `azure`
- imports containing `azure.functions`, `@azure/`, or `Microsoft.Azure.`
  - provider `azure`

## Stop Conditions

- Stop when more than one provider is plausible and the task is not a declared comparative experiment.
- Stop when the user asks for a provider-neutral repo but the requested managed service is provider-specific.
- Stop when repo signals and explicit user language conflict, unless the user explicitly says to migrate from one provider to another.
- Stop when no provider is named and the next workflow would generate cloud resources with provider-specific identity, state, or resource names.

## Routing Examples

- "add an s3-triggered lambda" -> `aws`
- "deploy on Cloud Run with Pub/Sub" -> `gcp`
- "bind a Key Vault secret to an Azure Function" -> `azure`
- "compare AWS vs GCP vs Azure for object intake" -> comparative provider path, not a single provider

