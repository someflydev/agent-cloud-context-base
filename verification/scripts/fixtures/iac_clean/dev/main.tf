variable "environment" {
  default = "dev"
}

resource "aws_s3_bucket" "assets" {
  bucket = "fixture-${var.environment}-assets"
}
