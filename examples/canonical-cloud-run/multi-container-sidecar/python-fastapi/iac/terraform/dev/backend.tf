terraform {
  backend "gcs" {
    bucket = "accb-dev-terraform-state"
    prefix = "cloudrun/multi-container-sidecar/dev"
  }
}
