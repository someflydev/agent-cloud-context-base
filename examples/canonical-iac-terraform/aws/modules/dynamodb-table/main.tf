variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "aws_dynamodb_table" "this" {
  name         = "${var.name_prefix}-${var.environment}-state"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }
}
