# Terraform aws starter

This starter keeps dev and test state separate.

```bash
cd infra/terraform/aws/dev
terraform init -backend-config=backend.tf
terraform plan -var-file=dev.tfvars

cd ../test
terraform init -backend-config=backend.tf
terraform plan -var-file=test.tfvars
```

Dev state: `{{state_backend_dev}}`. Test state: `{{state_backend_test}}`.
