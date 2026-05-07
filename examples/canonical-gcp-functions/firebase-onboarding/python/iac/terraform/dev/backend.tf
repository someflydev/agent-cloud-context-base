terraform {
  backend "gcs" {
    bucket = "accb-dev-tfstate"
    prefix = "accb/canonical-gcp-functions/firebase-onboarding/dev/terraform.tfstate"
  }
}
