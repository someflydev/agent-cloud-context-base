variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "google_storage_bucket" "this" {
  name                        = "${var.name_prefix}-${var.environment}-artifacts"
  location                    = "US"
  uniform_bucket_level_access = true
}

output "bucket_name" { value = google_storage_bucket.this.name }
