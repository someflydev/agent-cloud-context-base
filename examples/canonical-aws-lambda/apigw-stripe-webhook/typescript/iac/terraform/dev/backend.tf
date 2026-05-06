terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "accb/canonical-aws-lambda/apigw-stripe-webhook/typescript/dev.tfstate"
    region = "us-east-1"
  }
}
