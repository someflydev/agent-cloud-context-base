variable "environment" { type = string }
variable "env_var_prefix" { type = string }
variable "secret_path" { type = string }
variable "resource_prefix" { type = string }

provider "aws" {
  region = "us-east-1"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src"
  output_path = "${path.module}/function.zip"
}

resource "aws_s3_bucket" "source" {
  bucket = "${var.resource_prefix}-source-${var.environment}"
}

resource "aws_s3_bucket" "dest" {
  bucket = "${var.resource_prefix}-dest-${var.environment}"
}

resource "aws_sqs_queue" "dlq" {
  name = "${var.resource_prefix}-dlq-${var.environment}"
}

resource "aws_sqs_queue" "jobs" {
  name                       = "${var.resource_prefix}-jobs-${var.environment}"
  visibility_timeout_seconds = 120
  redrive_policy             = jsonencode({ deadLetterTargetArn = aws_sqs_queue.dlq.arn, maxReceiveCount = 3 })
}

resource "aws_dynamodb_table" "jobs" {
  name         = "${var.resource_prefix}-jobs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_iam_role" "lambda" {
  name               = "${var.resource_prefix}-lambda-${var.environment}"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_access" {
  name = "${var.resource_prefix}-access-${var.environment}"
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["s3:GetObject"], Resource = "${aws_s3_bucket.source.arn}/*" },
      { Effect = "Allow", Action = ["s3:PutObject"], Resource = "${aws_s3_bucket.dest.arn}/*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = aws_dynamodb_table.jobs.arn },
      { Effect = "Allow", Action = ["translate:TranslateText"], Resource = "*" },
      { Effect = "Allow", Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"], Resource = aws_sqs_queue.jobs.arn }
    ]
  })
}

resource "aws_lambda_function" "handler" {
  function_name    = "${var.resource_prefix}-handler-${var.environment}"
  role             = aws_iam_role.lambda.arn
  runtime          = "python3.12"
  handler          = "handler.lambda_handler"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 60
  environment {
    variables = {
      TABLE_NAME     = aws_dynamodb_table.jobs.name
      SOURCE_BUCKET  = aws_s3_bucket.source.bucket
      DEST_BUCKET    = aws_s3_bucket.dest.bucket
      ENV_VAR_PREFIX = var.env_var_prefix
      SECRET_PATH    = var.secret_path
    }
  }
}

resource "aws_lambda_event_source_mapping" "jobs" {
  event_source_arn = aws_sqs_queue.jobs.arn
  function_name    = aws_lambda_function.handler.arn
  batch_size       = 1
}
