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
  default = "gcr.io/example/accb-test-cloudrun-sidecar:latest"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name_prefix = "accb-${var.environment}-cloudrun-sidecar"
  labels      = { managed_by = "accb", environment = var.environment, family = "canonical-cloud-run" }
}

resource "google_service_account" "service" {
  account_id   = "${local.name_prefix}-svc"
  display_name = "accb ${var.environment} Cloud Run sidecar"
}

resource "google_logging_metric" "requests" {
  name   = "${local.name_prefix}-requests"
  filter = "resource.type=\"cloud_run_revision\""
}

resource "google_cloud_run_v2_service" "service" {
  name     = "${local.name_prefix}-svc"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"
  labels   = local.labels

  template {
    service_account = google_service_account.service.email
    containers {
      name  = "app"
      image = var.image
      ports {
        container_port = 8080
      }
      env {
        name  = "OTEL_EXPORTER_OTLP_ENDPOINT"
        value = "http://127.0.0.1:4318"
      }
      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }
      startup_probe {
        http_get {
          path = "/readyz"
          port = 8080
        }
      }
    }
    containers {
      name  = "otel"
      image = "otel/opentelemetry-collector@sha256:0000000000000000000000000000000000000000000000000000000000000000"
      args  = ["--config=/etc/otelcol/config.yaml"]
      resources {
        limits = {
          cpu    = "250m"
          memory = "256Mi"
        }
      }
    }
  }
}
