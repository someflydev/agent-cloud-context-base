terraform {
  backend "gcs" {
    bucket = "accb-dev-tfstate"
    prefix = "accb/canonical-gcp-functions/gcs-trigger-ocr-to-firestore/dev/terraform.tfstate"
  }
}
