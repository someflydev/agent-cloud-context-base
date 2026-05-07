variable "environment" { type = string }
variable "name_prefix" { type = string }

resource "aws_sqs_queue" "dlq" {
  name = "${var.name_prefix}-${var.environment}-dlq"
}

resource "aws_sqs_queue" "main" {
  name = "${var.name_prefix}-${var.environment}-main"
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })
}

output "queue_url" { value = aws_sqs_queue.main.url }
output "queue_arn" { value = aws_sqs_queue.main.arn }
