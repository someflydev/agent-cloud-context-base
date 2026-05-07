terraform {
  backend "gcs" {
    bucket = "accb-test-tfstate"
    prefix = "accb/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/test/terraform.tfstate"
  }
}
