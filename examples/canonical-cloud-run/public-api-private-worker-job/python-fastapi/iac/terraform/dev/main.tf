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
  default = "gcr.io/example/accb-dev-cloudrun-public-worker:latest"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name_prefix = "accb-${var.environment}-cloudrun-public-worker"
  labels      = { managed_by = "accb", environment = var.environment, family = "canonical-cloud-run" }
}

resource "google_service_account" "service" {
  account_id   = "${local.name_prefix}-svc"
  display_name = "accb ${var.environment} Cloud Run public worker"
}

resource "google_pubsub_topic" "review" {
  name   = "${local.name_prefix}-review"
  labels = local.labels
}

resource "google_storage_bucket" "attachments" {
  name                        = "${local.name_prefix}-attachments"
  location                    = var.region
  uniform_bucket_level_access = true
  labels                      = local.labels
}

resource "google_firestore_database" "workflow" {
  name        = "${local.name_prefix}-workflow"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

resource "google_secret_manager_secret" "reviewer" {
  secret_id = "${local.name_prefix}-reviewer"
  replication {
    auto {}
  }
  labels = local.labels
}

resource "google_cloud_run_v2_service" "public_api" {
  name     = "${local.name_prefix}-public"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"
  labels   = local.labels

  template {
    service_account = google_service_account.service.email
    containers {
      image = var.image
      env {
        name  = "ATTACHMENT_BUCKET"
        value = google_storage_bucket.attachments.name
      }
      env {
        name  = "REVIEW_TOPIC"
        value = google_pubsub_topic.review.name
      }
    }
  }
}

resource "google_cloud_run_v2_service" "private_worker" {
  name     = "${local.name_prefix}-private-worker"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"
  labels   = local.labels

  template {
    service_account = google_service_account.service.email
    containers {
      image = var.image
      env {
        name  = "REVIEWER_SECRET"
        value = google_secret_manager_secret.reviewer.secret_id
      }
      env {
        name  = "CALLBACK_AUDIENCE"
        value = "${local.name_prefix}-private-worker"
      }
    }
  }
}

resource "google_cloud_run_v2_job" "nightly_cleanup" {
  name     = "${local.name_prefix}-cleanup"
  location = var.region
  labels   = local.labels

  template {
    template {
      service_account = google_service_account.service.email
      containers {
        image = var.image
        args  = ["/cleanup"]
      }
      max_retries = 1
    }
  }
}

resource "google_cloud_run_service_iam_member" "private_worker_invoker" {
  location = google_cloud_run_v2_service.private_worker.location
  service  = google_cloud_run_v2_service.private_worker.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.service.email}"
}
