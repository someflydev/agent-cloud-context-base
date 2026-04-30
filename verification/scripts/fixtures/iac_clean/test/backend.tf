terraform {
  backend "s3" {
    bucket = "accb-state"
    key    = "test/terraform.tfstate"
  }
}
