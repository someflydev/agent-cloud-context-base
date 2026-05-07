terraform {
  backend "gcs" {
    bucket = "accb-dev-tfstate"
    prefix = "accb/canonical-gcp-functions/pubsub-translation-stream/dev/terraform.tfstate"
  }
}
