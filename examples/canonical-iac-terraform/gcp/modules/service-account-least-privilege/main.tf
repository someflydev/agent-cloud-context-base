variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "bucket_name" { type = string }
variable "topic_name" { type = string }
variable "secret_id" { type = string }

resource "google_service_account" "this" {
  account_id   = "${var.name_prefix}-${var.environment}-runtime"
  display_name = "accb ${var.environment} runtime"
}

output "email" { value = google_service_account.this.email }
