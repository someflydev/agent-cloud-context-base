terraform {
  backend "gcs" {
    bucket = "accb-test-tfstate"
    prefix = "accb/canonical-gcp-functions/http-stripe-webhook/test/terraform.tfstate"
  }
}
