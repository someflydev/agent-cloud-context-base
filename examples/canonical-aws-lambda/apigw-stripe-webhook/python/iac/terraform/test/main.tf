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

resource "aws_dynamodb_table" "events" {
  name         = "${var.resource_prefix}-events-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_iam_role" "workflow" {
  name               = "${var.resource_prefix}-workflow-${var.environment}"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "states.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}

resource "aws_sfn_state_machine" "fulfillment" {
  name       = "${var.resource_prefix}-workflow-${var.environment}"
  role_arn   = aws_iam_role.workflow.arn
  definition = jsonencode({ StartAt = "Accepted", States = { Accepted = { Type = "Succeed" } } })
}

resource "aws_apigatewayv2_api" "webhook" {
  name          = "${var.resource_prefix}-api-${var.environment}"
  protocol_type = "HTTP"
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
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.events.arn },
      { Effect = "Allow", Action = ["states:StartExecution"], Resource = aws_sfn_state_machine.fulfillment.arn },
      { Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = "*" }
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
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME     = aws_dynamodb_table.events.name
      WORKFLOW_ARN   = aws_sfn_state_machine.fulfillment.arn
      STRIPE_SECRET  = var.secret_path
      ENV_VAR_PREFIX = var.env_var_prefix
    }
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.webhook.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.handler.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "webhook" {
  api_id    = aws_apigatewayv2_api.webhook.id
  route_key = "POST /stripe/webhook"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowApiGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.webhook.execution_arn}/*/*"
}
