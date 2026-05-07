variable "environment" {
  type    = string
  default = "test"
}

locals {
  name_prefix = "accb-aws-${var.environment}-multi-role-platform"
  secret_path = "/accb/eks/multi-role-platform/test/workload"
}

resource "null_resource" "cluster_contract" {
  triggers = {
    name        = local.name_prefix
    environment = var.environment
    secret_path = local.secret_path
    provider    = "aws"
    services    = "MSK, S3, DynamoDB, IRSA, KEDA Kafka scaler"
  }
}

output "cluster_name" {
  value = local.name_prefix
}
