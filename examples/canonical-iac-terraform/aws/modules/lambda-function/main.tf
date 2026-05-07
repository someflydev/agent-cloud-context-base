variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "role_arn" { type = string }

resource "aws_lambda_function" "this" {
  function_name = "${var.name_prefix}-${var.environment}-handler"
  role          = var.role_arn
  runtime       = "python3.12"
  handler       = "handler.main"
  filename      = "placeholder.zip"
}
