# Stack Router

The stack router decides which provider, runtime, and language stack file or role pack should be loaded after the provider, runtime, and language axes are known. It does not infer the task workflow, archetype, scenario, or IaC tool by itself; it maps completed routing decisions to `context/stacks/` files.

## Core Rule

Load one primary runtime stack for the selected provider, runtime tier, and language, then add only the cross-cutting stack packs activated by explicit capabilities.

## Mappings / Signals

- AWS + function + python
  - load `context/stacks/aws-lambda-python.md`
- AWS + function + typescript
  - load `context/stacks/aws-lambda-typescript-node.md`
- AWS + function + node
  - load `context/stacks/aws-lambda-typescript-node.md`
- AWS + function + go
  - load `context/stacks/aws-lambda-go.md`
- GCP + function + python
  - load `context/stacks/gcp-cloudfn-python.md`
- GCP + function + typescript
  - load `context/stacks/gcp-cloudfn-typescript-node.md`
- GCP + function + node
  - load `context/stacks/gcp-cloudfn-typescript-node.md`
- GCP + function + go
  - load `context/stacks/gcp-cloudfn-go.md`
- Azure + function + python
  - load `context/stacks/azure-fn-python.md`
- Azure + function + typescript
  - load `context/stacks/azure-fn-typescript-node.md`
- Azure + function + node
  - load `context/stacks/azure-fn-typescript-node.md`
- Azure + function + dotnet
  - load `context/stacks/azure-fn-dotnet-isolated.md`
- GCP + managed-container + python + fastapi
  - load `context/stacks/cloudrun-python-fastapi.md`
- GCP + managed-container + typescript + hono
  - load `context/stacks/cloudrun-typescript-hono.md`
- GCP + managed-container + go + echo
  - load `context/stacks/cloudrun-go-echo.md`
- AWS + managed-container + python + fastapi
  - load `context/stacks/apprunner-python-fastapi.md`
- AWS + managed-container + typescript + hono
  - load `context/stacks/apprunner-typescript-hono.md`
- AWS + managed-container + go + echo
  - load `context/stacks/apprunner-go-echo.md`
- Azure + managed-container + python + fastapi
  - load `context/stacks/aca-python-fastapi.md`
- Azure + managed-container + dotnet
  - load `context/stacks/aca-dotnet-aspnet.md`
- Azure + managed-container + jobs
  - load `context/stacks/aca-jobs.md`
- AWS + k8s
  - load `context/stacks/eks-base.md`
  - add role packs for active workload roles
- GCP + k8s
  - load `context/stacks/gke-base.md`
  - add role packs for active workload roles
- Azure + k8s
  - load `context/stacks/aks-base.md`
  - add role packs for active workload roles
- k8s API role
  - load `context/stacks/k8s-api-workload.md`
- k8s worker role
  - load `context/stacks/k8s-worker-workload.md`
- k8s job role
  - load `context/stacks/k8s-job-workload.md`
- k8s cronjob role
  - load `context/stacks/k8s-cronjob-workload.md`
- k8s control-plane role
  - load `context/stacks/k8s-control-plane-workload.md`
- secrets + AWS
  - load `context/stacks/secrets-aws-secrets-manager.md`
- secrets + GCP
  - load `context/stacks/secrets-gcp-secret-manager.md`
- secrets + Azure
  - load `context/stacks/secrets-azure-key-vault.md`
- eventing + AWS
  - load `context/stacks/eventing-aws-eventbridge-sqs-sns.md`
- eventing + GCP
  - load `context/stacks/eventing-gcp-pubsub.md`
- eventing + Azure
  - load `context/stacks/eventing-azure-servicebus-eventgrid.md`
- storage + AWS
  - load `context/stacks/storage-aws-s3-dynamodb-rds.md`
- storage + GCP
  - load `context/stacks/storage-gcp-gcs-firestore-cloudsql.md`
- storage + Azure
  - load `context/stacks/storage-azure-blob-cosmos-azuresql.md`
- identity + AWS
  - load `context/stacks/identity-aws-iam.md`
- identity + GCP
  - load `context/stacks/identity-gcp-iam-sa.md`
- identity + Azure
  - load `context/stacks/identity-azure-entra-mi.md`
- observability
  - load `context/stacks/observability-otel-cloud.md`

## Stop Conditions

- Stop when provider, runtime tier, or language is unknown after the earlier routers have run.
- Stop when no stack file exists for the selected provider, runtime tier, and language cell.
- Stop when two primary runtime stacks match and the user did not request a comparative or migration task.
- Stop when a cross-cutting capability is required but its provider-specific stack pack is not planned.

## Routing Examples

- "AWS Lambda in Python" -> `context/stacks/aws-lambda-python.md`
- "Cloud Run FastAPI service" -> `context/stacks/cloudrun-python-fastapi.md`
- "App Runner Go Echo service with SQS" -> `context/stacks/apprunner-go-echo.md` + `context/stacks/eventing-aws-eventbridge-sqs-sns.md`
- "AKS API plus workers and crons" -> `context/stacks/aks-base.md` + role packs

