# Task Router

The task router decides which workflow file or small workflow chain should be loaded for a user request. It does not decide provider, runtime tier, language, IaC tool, archetype, scenario, or stack pack; those axes are handled by the other routers before the bundle assembler combines the result.

## Core Rule

Route by the cloud work the user is trying to complete, then load the smallest workflow set that can execute that work without guessing provider, runtime, or IaC details.

## Mappings / Signals

- "add a function", "new lambda", "new cloud function", "new azure function"
  - load `context/workflows/add-cloud-function.md`
- "add an s3-triggered lambda", "s3 put event"
  - load `context/workflows/add-aws-lambda-trigger.md`
- "add a cloud function for gcs object", "pub/sub-triggered cloud function"
  - load `context/workflows/add-gcp-cloud-function-trigger.md`
- "add a blob-triggered azure function", "service bus trigger"
  - load `context/workflows/add-azure-function-trigger.md`
- "deploy on cloud run", "containerize as cloud run service"
  - load `context/workflows/add-managed-container-service.md`
- "deploy on app runner", "container apps service"
  - load `context/workflows/add-managed-container-service.md`
- "add an api workload", "add a worker", "add a job", "add a cronjob"
  - load `context/workflows/add-k8s-workload-role.md`
- "set up terraform for dev and test", "pulumi stack"
  - load `context/workflows/add-iac-stack.md`
  - load `context/workflows/add-iac-isolation-pair.md`
- "bind a secret", "use secrets manager", "key vault binding"
  - load `context/workflows/add-secret-binding.md`
- "add a queue", "add an event bus seam", "dlq"
  - load `context/workflows/add-eventing-seam.md`
- "wire s3", "wire gcs", "wire blob storage"
  - load `context/workflows/add-cloud-storage-integration.md`
- "wire dynamodb", "wire cosmos", "wire firestore", "wire cloud sql", "wire rds", "wire azure sql"
  - load `context/workflows/add-cloud-database-integration.md`
- "private vpc", "vpc connector", "private endpoint"
  - load `context/workflows/add-vpc-private-network-path.md`
- "iam role", "service account", "managed identity binding"
  - load `context/workflows/add-identity-binding.md`
- "structured logs", "otel", "tracing"
  - load `context/workflows/add-observability-bundle.md`
- "smoke test for my function", "smoke test for my container", "smoke test for my pod"
  - load `context/workflows/add-cloud-smoke-tests.md`
- "integration test", "ephemeral test stack", "localstack", "emulator", "azurite"
  - load `context/workflows/add-cloud-integration-tests.md`
- "replay", "dlq handling", "exactly-once"
  - load `context/workflows/add-replay-and-dlq-handling.md`
- "container image", "dockerfile", "registry"
  - load `context/workflows/add-cloud-runtime-image.md`
- "helm chart", "kustomize overlay"
  - load `context/workflows/add-helm-or-kustomize-overlay.md`
- "promote dev to test"
  - load `context/workflows/promote-dev-to-test.md`
- "bootstrap a cloud repo", "new repo from accb"
  - load `context/workflows/bootstrap-cloud-repo.md`
  - prefer `scripts/new_cloud_repo.py` after PROMPT_16 over manual scaffolding
- "generate from scenario", "turn this cloud prompt into a repo", "claims intake prompt", "excellent cloud prompt"
  - load `context/workflows/plan-scenario-derived-repo.md`
  - load `context/router/scenario-router.md`
- "make a prompt sequence"
  - load `context/workflows/generate-prompt-sequence.md`
- "post-flight cleanup before commit"
  - load `context/workflows/post-flight-refinement.md`
- "refresh mermaid diagrams"
  - load `context/workflows/refresh-mermaid-diagrams.md`
- "refactor"
  - load `context/workflows/refactor.md`
- "fix bug", "bug fix", "regression"
  - load `context/workflows/fix-bug.md`

## Compound Requests

- "add an s3-triggered lambda with secret binding and ephemeral integration tests"
  - load `context/workflows/add-aws-lambda-trigger.md`
  - load `context/workflows/add-secret-binding.md`
  - load `context/workflows/add-iac-isolation-pair.md`
  - load `context/workflows/add-cloud-integration-tests.md`
- "deploy a Cloud Run API with a private worker, Secret Manager, and structured tracing"
  - load `context/workflows/add-managed-container-service.md`
  - load `context/workflows/add-secret-binding.md`
  - load `context/workflows/add-vpc-private-network-path.md`
  - load `context/workflows/add-observability-bundle.md`
- "add an Azure blob-triggered function with Cosmos persistence and DLQ replay"
  - load `context/workflows/add-azure-function-trigger.md`
  - load `context/workflows/add-cloud-database-integration.md`
  - load `context/workflows/add-eventing-seam.md`
  - load `context/workflows/add-replay-and-dlq-handling.md`
- "create k8s API, worker, cronjob, and Helm overlay"
  - load `context/workflows/add-k8s-workload-role.md`
  - load `context/workflows/add-helm-or-kustomize-overlay.md`
  - load `context/workflows/add-cloud-smoke-tests.md`
- "set up Pulumi dev/test stacks for App Runner with an SQS queue"
  - load `context/workflows/add-iac-stack.md`
  - load `context/workflows/add-iac-isolation-pair.md`
  - load `context/workflows/add-managed-container-service.md`
  - load `context/workflows/add-eventing-seam.md`
- "plan a claims intake repo from a prompt with uploads, review events, and nightly escalation"
  - load `context/workflows/plan-scenario-derived-repo.md`
  - load `context/router/scenario-router.md`
  - load `context/workflows/add-iac-isolation-pair.md`

## Stop Conditions

- Stop when the task names only a provider service and no workload action is clear.
- Stop when a single request implies incompatible workflows, such as replacing a function with Kubernetes while also asking for a no-architecture-change patch.
- Stop when required dev/test isolation details are missing for a workflow that generates cloud resources.
- Stop when the request activates provider-specific trigger behavior but the provider router cannot choose one provider.

## Routing Examples

- "add an s3-triggered lambda" -> `context/workflows/add-aws-lambda-trigger.md`
- "deploy this on Cloud Run with a secret" -> `context/workflows/add-managed-container-service.md` + `context/workflows/add-secret-binding.md`
- "bootstrap a cloud repo from accb" -> `context/workflows/bootstrap-cloud-repo.md`
- "refresh mermaid diagrams" -> `context/workflows/refresh-mermaid-diagrams.md`

