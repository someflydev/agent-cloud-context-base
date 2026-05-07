variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "google_secret_manager_secret" "this" {
  secret_id = "${var.name_prefix}-${var.environment}-config"
  replication {
    auto {}
  }
}

output "secret_id" { value = google_secret_manager_secret.this.secret_id }
