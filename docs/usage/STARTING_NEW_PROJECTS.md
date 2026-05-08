# Starting New Projects

Start by declaring the cloud profile:

- Provider: `aws`, `gcp`, or `azure`.
- Runtime tier: `function`, `managed_container`, or `k8s`.
- Primary language and stack.
- IaC tool.
- Dev/test isolation: separate state, env-var prefixes, secret paths, and resource names.

## Function Example

```bash
python3 scripts/new_cloud_repo.py \
  --archetype cloud-function-repo \
  --provider aws --runtime-tier function \
  --primary-stack aws-lambda-python --primary-language python \
  --iac-tool pulumi-python \
  --manifest func-aws-lambda-python \
  --support-service aws-s3 --support-service aws-dynamodb \
  --support-service aws-secrets-manager \
  --include-local-provider \
  --include-secret-binding-example \
  --include-observability-bundle \
  --target-dir /tmp/accb-new-function
```

## Container Example

```bash
python3 scripts/new_cloud_repo.py \
  --archetype managed-container-multi-service \
  --provider gcp --runtime-tier managed_container \
  --primary-stack cloudrun-python-fastapi --primary-language python \
  --iac-tool pulumi-python \
  --manifest container-cloudrun-fastapi \
  --scenario-pattern container.public-api-private-worker-job \
  --support-service gcp-gcs --support-service gcp-secret-manager \
  --include-secret-binding-example \
  --include-observability-bundle \
  --target-dir /tmp/accb-new-container
```

## Kubernetes Example

This example starts from the scenario pattern `k8s.multi-role-platform` and resolves to AKS .NET with Pulumi .NET:

```bash
python3 scripts/new_cloud_repo.py \
  --archetype k8s-platform-repo \
  --provider azure --runtime-tier k8s \
  --primary-stack aks-base --primary-language dotnet \
  --iac-tool pulumi-dotnet \
  --manifest k8s-aks-multi-role-dotnet \
  --scenario-pattern k8s.multi-role-platform \
  --support-service azure-key-vault --support-service azure-servicebus \
  --include-secret-binding-example \
  --include-observability-bundle \
  --target-dir /tmp/accb-new-k8s
```

After generation, enter the repo and run:

```bash
python3 scripts/work.py resume
python3 .accb/scripts/accb_verify.py
python3 .accb/scripts/accb_inspect.py
```
