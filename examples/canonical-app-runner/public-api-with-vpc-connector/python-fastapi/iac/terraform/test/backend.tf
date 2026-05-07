terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "apprunner/public-api-with-vpc-connector/test/terraform.tfstate"
    region = "us-east-1"
  }
}
