variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "service_email" { type = string }

resource "google_cloudfunctions2_function" "this" {
  name     = "${var.name_prefix}-${var.environment}-handler"
  location = "us-central1"
  build_config {
    runtime     = "python312"
    entry_point = "main"
  }
  service_config {
    service_account_email = var.service_email
  }
}
