variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "google_pubsub_topic" "dlq" {
  name = "${var.name_prefix}-${var.environment}-dlq"
}

resource "google_pubsub_topic" "main" {
  name = "${var.name_prefix}-${var.environment}-main"
}

resource "google_pubsub_subscription" "main" {
  name  = "${var.name_prefix}-${var.environment}-sub"
  topic = google_pubsub_topic.main.name
  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }
}

output "topic_name" { value = google_pubsub_topic.main.name }
