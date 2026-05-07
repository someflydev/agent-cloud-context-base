variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "google_firestore_database" "this" {
  name        = "${var.name_prefix}-${var.environment}-db"
  location_id = "nam5"
  type        = "FIRESTORE_NATIVE"
}
