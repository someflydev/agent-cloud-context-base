terraform {
  backend "gcs" {
    bucket = "accb-test-terraform-state"
    prefix = "cloudrun/cloudrun-job-nightly-report/test"
  }
}
