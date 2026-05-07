variable "environment" {
  type    = string
  default = "dev"
}

locals {
  name_prefix = "accb-azure-${var.environment}-multi-role-platform"
  secret_path = "https://accb-kv.vault.azure.net/secrets/aks-multi-role-platform/dev/workload"
}

resource "null_resource" "cluster_contract" {
  triggers = {
    name        = local.name_prefix
    environment = var.environment
    secret_path = local.secret_path
    provider    = "azure"
    services    = "Cosmos DB, Azure SQL, Service Bus, AKS Workload Identity, KEDA Service Bus scaler"
  }
}

output "cluster_name" {
  value = local.name_prefix
}
