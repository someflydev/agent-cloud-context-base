terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.30" }
  }
}

variable "environment" { type = string }
variable "project_id" { type = string }
variable "region" { type = string }
variable "image" {
  type    = string
  default = "gcr.io/example/accb-dev-cloudrun-nightly-report:latest"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name_prefix = "accb-${var.environment}-cloudrun-nightly-report"
  labels      = { managed_by = "accb", environment = var.environment, family = "canonical-cloud-run" }
}

resource "google_service_account" "job" {
  account_id   = "${local.name_prefix}-job"
  display_name = "accb ${var.environment} Cloud Run nightly report job"
}

resource "google_storage_bucket" "reports" {
  name                        = "${local.name_prefix}-reports"
  location                    = var.region
  uniform_bucket_level_access = true
  labels                      = local.labels
}

resource "google_secret_manager_secret" "reporting" {
  secret_id = "${local.name_prefix}-reporting"
  replication {
    auto {}
  }
  labels = local.labels
}

resource "google_cloud_run_v2_job" "nightly_report" {
  name     = "${local.name_prefix}-job"
  location = var.region
  labels   = local.labels

  template {
    template {
      service_account = google_service_account.job.email
      containers {
        image = var.image
        args  = ["/cleanup"]
        env {
          name  = "REPORT_BUCKET"
          value = google_storage_bucket.reports.name
        }
        env {
          name  = "REPORTING_SECRET"
          value = google_secret_manager_secret.reporting.secret_id
        }
      }
      max_retries = 1
      timeout     = "900s"
    }
  }
}

resource "google_cloud_scheduler_job" "nightly" {
  name      = "${local.name_prefix}-schedule"
  region    = var.region
  schedule  = "0 6 * * *"
  time_zone = "Etc/UTC"

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.nightly_report.name}:run"
    oauth_token {
      service_account_email = google_service_account.job.email
    }
  }
}
