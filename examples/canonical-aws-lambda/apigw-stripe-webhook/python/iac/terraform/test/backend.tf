terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "accb/canonical-aws-lambda/apigw-stripe-webhook/python/test.tfstate"
    region = "us-east-1"
  }
}
