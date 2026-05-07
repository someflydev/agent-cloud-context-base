terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "canonical-iac-terraform/aws/test/terraform.tfstate"
    region = "us-east-1"
  }
}
