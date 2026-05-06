terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "accb/canonical-aws-lambda/sqs-document-translation/go/test.tfstate"
    region = "us-east-1"
  }
}
