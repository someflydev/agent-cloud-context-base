terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "accb/canonical-aws-lambda/apigw-stripe-webhook/typescript/test.tfstate"
    region = "us-east-1"
  }
}
