terraform {
  backend "gcs" {
    bucket = "accb-dev-tfstate"
    prefix = "accb/canonical-gcp-functions/eventarc-monitoring-router/dev/terraform.tfstate"
  }
}
