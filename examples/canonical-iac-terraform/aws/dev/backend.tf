terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "canonical-iac-terraform/aws/dev/terraform.tfstate"
    region = "us-east-1"
  }
}
