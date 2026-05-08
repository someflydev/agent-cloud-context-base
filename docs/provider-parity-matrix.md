# Provider Parity Matrix

Generated from `verification/stack_support_matrix.yaml` by `scripts/render_parity_matrix.py`.

| Provider | Runtime tier | Platform / tool | Language / variant | Status | Canonical example | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| aws | managed_container | app-runner | python-fastapi | Supported | [canonical-app-runner/public-api-with-vpc-connector](../examples/canonical-app-runner/public-api-with-vpc-connector/go-echo/) |  |
| aws | managed_container | app-runner | go-echo | Supported | [canonical-app-runner/public-api-with-vpc-connector](../examples/canonical-app-runner/public-api-with-vpc-connector/go-echo/) |  |
| aws | managed_container | app-runner | supplier-onboarding | Supported | [canonical-app-runner/supplier-onboarding](../examples/canonical-app-runner/supplier-onboarding/python-fastapi/) |  |
| aws | function | aws-lambda | python | Supported | [canonical-aws-lambda/s3-trigger-image-moderation](../examples/canonical-aws-lambda/s3-trigger-image-moderation/go/) |  |
| aws | function | aws-lambda | typescript | Supported | [canonical-aws-lambda/apigw-stripe-webhook](../examples/canonical-aws-lambda/apigw-stripe-webhook/python/) |  |
| aws | function | aws-lambda | go | Supported | [canonical-aws-lambda/sqs-document-translation](../examples/canonical-aws-lambda/sqs-document-translation/python/) |  |
| aws | function | aws-lambda | java | Deferred |  | rare JVM-oriented Lambda cases remain deferred outside this arc |
| aws | function | aws-lambda | dotnet | Not Planned |  | not planned for the canonical AWS Lambda arc |
| aws | function | aws-lambda | ruby | Not Planned |  | not planned for the canonical AWS Lambda arc |
| aws | k8s | eks | python | Supported | [canonical-eks/multi-role-platform](../examples/canonical-eks/multi-role-platform/go/) |  |
| aws | k8s | eks | go | Supported | [canonical-eks/multi-role-platform](../examples/canonical-eks/multi-role-platform/go/) |  |
| gcp | managed_container | cloud-run | python-fastapi | Supported | [canonical-cloud-run/public-api-private-worker-job](../examples/canonical-cloud-run/public-api-private-worker-job/typescript-hono/) |  |
| gcp | managed_container | cloud-run | multi-container-sidecar | Supported | [canonical-cloud-run/multi-container-sidecar](../examples/canonical-cloud-run/multi-container-sidecar/python-fastapi/) |  |
| gcp | managed_container | cloud-run | go-echo | Supported | [canonical-cloud-run/public-api-private-worker-job](../examples/canonical-cloud-run/public-api-private-worker-job/typescript-hono/) |  |
| gcp | managed_container | cloud-run | typescript-hono | Supported | [canonical-cloud-run/public-api-private-worker-job](../examples/canonical-cloud-run/public-api-private-worker-job/typescript-hono/) |  |
| gcp | managed_container | cloud-run | cloudrun-job | Supported | [canonical-cloud-run/cloudrun-job-nightly-report](../examples/canonical-cloud-run/cloudrun-job-nightly-report/python-fastapi/) |  |
| gcp | function | gcp-cloud-functions | python | Supported | [canonical-gcp-functions/gcs-trigger-ocr-to-firestore](../examples/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/go/) |  |
| gcp | function | gcp-cloud-functions | typescript | Supported | [canonical-gcp-functions/http-stripe-webhook](../examples/canonical-gcp-functions/http-stripe-webhook/typescript/) |  |
| gcp | function | gcp-cloud-functions | go | Supported | [canonical-gcp-functions/eventarc-monitoring-router](../examples/canonical-gcp-functions/eventarc-monitoring-router/go/) |  |
| gcp | function | gcp-cloud-functions | java | Deferred |  | rare JVM-oriented Cloud Functions cases remain deferred outside this arc |
| gcp | function | gcp-cloud-functions | dotnet | Not Planned |  | not planned for the canonical GCP Cloud Functions arc |
| gcp | function | gcp-cloud-functions | ruby | Not Planned |  | not planned for the canonical GCP Cloud Functions arc |
| gcp | function | gcp-cloud-functions | php | Not Planned |  | not planned for the canonical GCP Cloud Functions arc |
| gcp | k8s | gke | python | Supported | [canonical-gke/multi-role-platform](../examples/canonical-gke/multi-role-platform/go/) |  |
| gcp | k8s | gke | go | Supported | [canonical-gke/multi-role-platform](../examples/canonical-gke/multi-role-platform/go/) |  |
| azure | managed_container | container-apps | python-fastapi | Supported | [canonical-container-apps/public-api-private-worker-jobs](../examples/canonical-container-apps/public-api-private-worker-jobs/typescript-hono/) |  |
| azure | managed_container | container-apps | dotnet-aspnet | Supported | [canonical-container-apps/public-api-private-worker-jobs](../examples/canonical-container-apps/public-api-private-worker-jobs/typescript-hono/) |  |
| azure | managed_container | container-apps | dapr | Supported | [canonical-container-apps/dapr-pubsub-binding](../examples/canonical-container-apps/dapr-pubsub-binding/dotnet-aspnet/) |  |
| azure | managed_container | container-apps | typescript-hono | Supported | [canonical-container-apps/public-api-private-worker-jobs](../examples/canonical-container-apps/public-api-private-worker-jobs/typescript-hono/) |  |
| azure | function | azure-functions | python | Supported | [canonical-azure-functions/blob-trigger-receipt-ocr](../examples/canonical-azure-functions/blob-trigger-receipt-ocr/dotnet-isolated/) |  |
| azure | function | azure-functions | typescript | Supported | [canonical-azure-functions/cosmos-changefeed-search-sync](../examples/canonical-azure-functions/cosmos-changefeed-search-sync/typescript/) |  |
| azure | function | azure-functions | dotnet-isolated | Supported | [canonical-azure-functions/servicebus-classification](../examples/canonical-azure-functions/servicebus-classification/dotnet-isolated/) |  |
| azure | function | azure-functions | powershell | Deferred |  | PowerShell remains reserved for ops-only Azure Functions cases |
| azure | k8s | aks | dotnet | Supported | [canonical-aks/multi-role-platform](../examples/canonical-aks/multi-role-platform/typescript/) |  |
| azure | k8s | aks | typescript | Supported | [canonical-aks/multi-role-platform](../examples/canonical-aks/multi-role-platform/typescript/) |  |
| iac | pulumi | typescript | aws | Supported | [canonical-iac-pulumi/typescript-aws](../examples/canonical-iac-pulumi/typescript/aws/) |  |
| iac | pulumi | typescript | gcp | Supported | [canonical-iac-pulumi/typescript-gcp](../examples/canonical-iac-pulumi/typescript/gcp/) |  |
| iac | pulumi | typescript | azure | Supported | [canonical-iac-pulumi/typescript-azure](../examples/canonical-iac-pulumi/typescript/azure/) |  |
| iac | pulumi | python | aws | Supported | [canonical-iac-pulumi/python-aws](../examples/canonical-iac-pulumi/python/aws/) |  |
| iac | pulumi | python | gcp | Supported | [canonical-iac-pulumi/python-gcp](../examples/canonical-iac-pulumi/python/gcp/) |  |
| iac | pulumi | python | azure | Supported | [canonical-iac-pulumi/python-azure](../examples/canonical-iac-pulumi/python/azure/) |  |
| iac | pulumi | go | aws | Supported | [canonical-iac-pulumi/go-aws](../examples/canonical-iac-pulumi/go/aws/) |  |
| iac | pulumi | go | gcp | Supported | [canonical-iac-pulumi/go-gcp](../examples/canonical-iac-pulumi/go/gcp/) |  |
| iac | pulumi | go | azure | Supported | [canonical-iac-pulumi/go-azure](../examples/canonical-iac-pulumi/go/azure/) |  |
| iac | pulumi | dotnet | azure | Supported | [canonical-iac-pulumi/dotnet-azure](../examples/canonical-iac-pulumi/dotnet/azure/) |  |
