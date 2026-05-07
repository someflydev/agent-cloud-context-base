terraform {
  backend "gcs" {
    bucket = "accb-test-tfstate"
    prefix = "accb/canonical-gcp-functions/firebase-onboarding/test/terraform.tfstate"
  }
}
