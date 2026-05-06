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

resource "aws_s3_bucket" "images" {
  bucket = "${var.resource_prefix}-images-${var.environment}"
}

resource "aws_dynamodb_table" "records" {
  name         = "${var.resource_prefix}-records-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_cloudwatch_event_bus" "flagged" {
  name = "${var.resource_prefix}-events-${var.environment}"
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
      { Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = aws_dynamodb_table.records.arn },
      { Effect = "Allow", Action = ["rekognition:DetectLabels", "rekognition:DetectModerationLabels"], Resource = "*" },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = aws_cloudwatch_event_bus.flagged.arn }
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
  timeout          = 30
  environment {
    variables = {
      TABLE_NAME     = aws_dynamodb_table.records.name
      EVENT_BUS_NAME = aws_cloudwatch_event_bus.flagged.name
      ENV_VAR_PREFIX = var.env_var_prefix
      SECRET_PATH    = var.secret_path
    }
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.handler.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.images.arn
}

resource "aws_s3_bucket_notification" "images" {
  bucket = aws_s3_bucket.images.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.handler.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.allow_s3]
}
