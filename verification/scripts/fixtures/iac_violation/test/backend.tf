terraform {
  backend "s3" {
    bucket = "accb-state"
    key    = "shared/terraform.tfstate"
  }
}
