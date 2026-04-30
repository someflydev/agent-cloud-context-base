resource "aws_s3_bucket" "assets" {
  bucket = "fixture-assets"
}

variable "password" {
  default = "not-a-real-password"
}
