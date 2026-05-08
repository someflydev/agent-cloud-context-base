terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "apprunner/public-api-with-vpc-connector/dev/terraform.tfstate"
    region = "us-east-1"
  }
}
