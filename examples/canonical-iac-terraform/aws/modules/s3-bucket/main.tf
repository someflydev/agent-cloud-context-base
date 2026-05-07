variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "aws_s3_bucket" "this" {
  bucket = "${var.name_prefix}-${var.environment}-artifacts"
}

output "bucket_name" { value = aws_s3_bucket.this.bucket }
output "bucket_arn" { value = aws_s3_bucket.this.arn }
