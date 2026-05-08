terraform {
  backend "s3" {
    bucket = "accb-terraform-state-test"
    key    = "canonical-aws-k8s/test/terraform.tfstate"
    region = "us-east-1"
  }
}
