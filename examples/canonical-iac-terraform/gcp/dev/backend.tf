terraform {
  backend "gcs" {
    bucket = "accb-dev-terraform-state"
    prefix = "canonical-iac-terraform/gcp/dev"
  }
}
