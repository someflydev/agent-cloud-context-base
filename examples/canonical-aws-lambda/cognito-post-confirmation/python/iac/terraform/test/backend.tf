terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "accb/canonical-aws-lambda/cognito-post-confirmation/python/test.tfstate"
    region = "us-east-1"
  }
}
