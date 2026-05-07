terraform {
  backend "s3" {
    bucket = "accb-dev-terraform-state"
    key    = "accb/canonical-aws-lambda/s3-trigger-image-moderation/typescript/dev.tfstate"
    region = "us-east-1"
  }
}
