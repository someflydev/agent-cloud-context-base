terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "accb/canonical-aws-lambda/eventbridge-cdc-relay/typescript/test.tfstate"
    region = "us-east-1"
  }
}
