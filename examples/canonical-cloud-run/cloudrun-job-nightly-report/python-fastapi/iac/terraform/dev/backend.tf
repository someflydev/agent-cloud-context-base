terraform {
  backend "gcs" {
    bucket = "accb-dev-terraform-state"
    prefix = "cloudrun/cloudrun-job-nightly-report/dev"
  }
}
