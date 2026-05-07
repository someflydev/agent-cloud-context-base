terraform {
  backend "s3" {
    bucket = "accb-terraform-state-dev"
    key    = "canonical-aws-k8s/dev/terraform.tfstate"
    region = "us-east-1"
  }
}
