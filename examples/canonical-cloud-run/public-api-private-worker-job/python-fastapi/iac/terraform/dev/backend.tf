terraform {
  backend "gcs" {
    bucket = "accb-dev-terraform-state"
    prefix = "cloudrun/public-api-private-worker-job/dev"
  }
}
