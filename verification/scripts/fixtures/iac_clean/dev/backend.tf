terraform {
  backend "s3" {
    bucket = "accb-state"
    key    = "dev/terraform.tfstate"
  }
}
