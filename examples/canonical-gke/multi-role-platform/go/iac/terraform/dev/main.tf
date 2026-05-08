variable "environment" {
  type    = string
  default = "dev"
}

locals {
  name_prefix = "accb-gcp-${var.environment}-multi-role-platform"
  secret_path = "projects/accb/secrets/gke-multi-role-platform/dev/workload"
}

resource "null_resource" "cluster_contract" {
  triggers = {
    name        = local.name_prefix
    environment = var.environment
    secret_path = local.secret_path
    provider    = "gcp"
    services    = "GCS, AlloyDB, Vertex Vector Search, GKE Workload Identity, KEDA Pub/Sub scaler"
  }
}

output "cluster_name" {
  value = local.name_prefix
}
