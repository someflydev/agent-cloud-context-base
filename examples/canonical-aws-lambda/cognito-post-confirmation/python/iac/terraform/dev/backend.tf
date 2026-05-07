terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "accb/canonical-aws-lambda/cognito-post-confirmation/python/dev.tfstate"
    region = "us-east-1"
  }
}
