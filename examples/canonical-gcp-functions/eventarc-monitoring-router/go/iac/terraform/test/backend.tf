terraform {
  backend "gcs" {
    bucket = "accb-test-tfstate"
    prefix = "accb/canonical-gcp-functions/eventarc-monitoring-router/test/terraform.tfstate"
  }
}
