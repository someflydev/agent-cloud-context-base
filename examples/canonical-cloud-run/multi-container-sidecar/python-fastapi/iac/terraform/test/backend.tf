terraform {
  backend "gcs" {
    bucket = "accb-test-terraform-state"
    prefix = "cloudrun/multi-container-sidecar/test"
  }
}
