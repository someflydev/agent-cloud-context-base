variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "secret_path" { type = string }

resource "aws_secretsmanager_secret" "this" {
  name = "${var.secret_path}/${var.environment}"
}

output "secret_arn" { value = aws_secretsmanager_secret.this.arn }
