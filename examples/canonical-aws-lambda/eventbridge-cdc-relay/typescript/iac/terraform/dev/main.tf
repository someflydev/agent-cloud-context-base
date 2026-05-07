variable "environment" { type = string }
variable "env_var_prefix" { type = string }
variable "secret_path" { type = string }
variable "resource_prefix" { type = string }

provider "aws" {
  region = "us-east-1"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../src/handler.js"
  output_path = "${path.module}/function.zip"
}

resource "aws_dynamodb_table" "changes" {
  name         = "${var.resource_prefix}-changes-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_cloudwatch_event_bus" "source" {
  name = "${var.resource_prefix}-source-${var.environment}"
}

resource "aws_cloudwatch_event_bus" "relay" {
  name = "${var.resource_prefix}-relay-${var.environment}"
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
      { Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = aws_dynamodb_table.changes.arn },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = aws_cloudwatch_event_bus.relay.arn }
    ]
  })
}

resource "aws_lambda_function" "handler" {
  function_name    = "${var.resource_prefix}-handler-${var.environment}"
  role             = aws_iam_role.lambda.arn
  runtime          = "nodejs20.x"
  handler          = "handler.handler"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME      = aws_dynamodb_table.changes.name
      RELAY_BUS_NAME  = aws_cloudwatch_event_bus.relay.name
      ENV_VAR_PREFIX  = var.env_var_prefix
      SECRET_PATH     = var.secret_path
    }
  }
}

resource "aws_cloudwatch_event_rule" "cdc" {
  name           = "${var.resource_prefix}-cdc-${var.environment}"
  event_bus_name = aws_cloudwatch_event_bus.source.name
  event_pattern  = jsonencode({ source = ["accb.database"] })
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule           = aws_cloudwatch_event_rule.cdc.name
  event_bus_name = aws_cloudwatch_event_bus.source.name
  arn            = aws_lambda_function.handler.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.handler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cdc.arn
}
