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
  name_prefix = "accb-${var.environment}-gcp-stripe"
  labels      = { managed_by = "accb", environment = var.environment, family = "canonical-gcp-functions" }
}

resource "google_service_account" "function" {
  account_id   = "${local.name_prefix}-fn"
  display_name = "accb ${var.environment} Stripe webhook function"
}

resource "google_secret_manager_secret" "stripe_signing" {
  secret_id = "${local.name_prefix}-signing"
  labels    = local.labels
  replication {
    auto {}
  }
}

resource "google_cloud_tasks_queue" "fulfillment" {
  name     = "${local.name_prefix}-fulfillment"
  location = var.region
}
