terraform {
  backend "gcs" {
    bucket = "accb-test-terraform-state"
    prefix = "cloudrun/public-api-private-worker-job/test"
  }
}
