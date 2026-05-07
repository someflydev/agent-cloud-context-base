terraform {
  backend "gcs" {
    bucket = "accb-test-tfstate"
    prefix = "accb/canonical-gcp-functions/pubsub-translation-stream/test/terraform.tfstate"
  }
}
