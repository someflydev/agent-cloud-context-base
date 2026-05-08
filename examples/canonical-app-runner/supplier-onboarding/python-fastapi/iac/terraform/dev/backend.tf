terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "apprunner/supplier-onboarding/dev/terraform.tfstate"
    region = "us-east-1"
  }
}
