terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "accb/canonical-aws-lambda/sqs-document-translation/go/dev.tfstate"
    region = "us-east-1"
  }
}
