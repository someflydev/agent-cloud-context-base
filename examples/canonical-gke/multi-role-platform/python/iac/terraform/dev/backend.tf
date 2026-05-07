terraform {
  backend "gcs" {
    bucket = "accb-terraform-state-dev"
    prefix = "canonical-gke/dev"
  }
}
