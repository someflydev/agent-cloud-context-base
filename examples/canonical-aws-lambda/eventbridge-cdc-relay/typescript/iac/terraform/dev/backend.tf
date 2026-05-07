terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "accb/canonical-aws-lambda/eventbridge-cdc-relay/typescript/dev.tfstate"
    region = "us-east-1"
  }
}
