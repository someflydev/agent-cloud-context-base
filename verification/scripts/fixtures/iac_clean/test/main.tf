variable "environment" {
  default = "test"
}

resource "aws_s3_bucket" "assets" {
  bucket = "fixture-${var.environment}-assets"
}
