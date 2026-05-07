terraform {
  backend "s3" {
    bucket = "accb-test-terraform-state"
    key    = "accb/canonical-aws-lambda/s3-trigger-image-moderation/typescript/test.tfstate"
    region = "us-east-1"
  }
}
