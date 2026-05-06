terraform {
  backend "gcs" {
    bucket = "accb-dev-tfstate"
    prefix = "accb/canonical-gcp-functions/http-stripe-webhook/dev/terraform.tfstate"
  }
}
