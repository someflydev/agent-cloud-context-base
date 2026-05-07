terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
  }
}

variable "environment" { type = string }
variable "project_id" { type = string }
variable "region" { type = string }

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name_prefix = "accb-${var.environment}-gcp-translation"
  labels      = { managed_by = "accb", environment = var.environment, family = "canonical-gcp-functions" }
}

resource "google_service_account" "function" {
  account_id   = "${local.name_prefix}-fn"
  display_name = "accb ${var.environment} Pub/Sub translation function"
}

resource "google_pubsub_topic" "source" {
  name   = "${local.name_prefix}-source"
  labels = local.labels
}

resource "google_pubsub_topic" "completion" {
  name   = "${local.name_prefix}-complete"
  labels = local.labels
}

resource "google_firestore_database" "default" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}
