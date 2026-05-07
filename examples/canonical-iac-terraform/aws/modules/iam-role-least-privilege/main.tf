variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "bucket_arn" { type = string }
variable "queue_arn" { type = string }
variable "secret_arn" { type = string }

resource "aws_iam_role" "this" {
  name = "${var.name_prefix}-${var.environment}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy" "least_privilege" {
  name = "${var.name_prefix}-${var.environment}-least-privilege"
  role = aws_iam_role.this.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["s3:GetObject", "s3:PutObject"], Resource = ["${var.bucket_arn}/*"] },
      { Effect = "Allow", Action = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage"], Resource = [var.queue_arn] },
      { Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = [var.secret_arn] }
    ]
  })
}

output "role_arn" { value = aws_iam_role.this.arn }
