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
  name_prefix = "accb-${var.environment}-gcp-monitoring-router"
  labels      = { managed_by = "accb", environment = var.environment, family = "canonical-gcp-functions" }
}

resource "google_service_account" "function" {
  account_id   = "${local.name_prefix}-fn"
  display_name = "accb ${var.environment} monitoring router function"
}

resource "google_bigquery_dataset" "audit" {
  dataset_id = replace("${local.name_prefix}_audit", "-", "_")
  location   = "US"
  labels     = local.labels
}

resource "google_secret_manager_secret" "slack_webhook" {
  secret_id = "${local.name_prefix}-slack"
  labels    = local.labels
  replication {
    auto {}
  }
}
