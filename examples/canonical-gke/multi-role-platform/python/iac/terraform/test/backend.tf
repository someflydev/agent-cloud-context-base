terraform {
  backend "gcs" {
    bucket = "accb-terraform-state-test"
    prefix = "canonical-gke/test"
  }
}
