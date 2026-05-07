terraform {
  backend "gcs" {
    bucket = "accb-test-terraform-state"
    prefix = "canonical-iac-terraform/gcp/test"
  }
}
