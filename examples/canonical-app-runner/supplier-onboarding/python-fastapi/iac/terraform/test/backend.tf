terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "apprunner/supplier-onboarding/test/terraform.tfstate"
    region = "us-east-1"
  }
}
