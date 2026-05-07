module "bucket" {
  source      = "../modules/s3-bucket"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "table" {
  source      = "../modules/dynamodb-table"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "queue" {
  source      = "../modules/sqs-queue-with-dlq"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "secret" {
  source      = "../modules/secrets-manager-secret"
  environment = var.environment
  name_prefix = var.name_prefix
  secret_path = var.secret_path
}

module "role" {
  source      = "../modules/iam-role-least-privilege"
  environment = var.environment
  name_prefix = var.name_prefix
  bucket_arn  = module.bucket.bucket_arn
  queue_arn   = module.queue.queue_arn
  secret_arn  = module.secret.secret_arn
}

module "function" {
  source      = "../modules/lambda-function"
  environment = var.environment
  name_prefix = var.name_prefix
  role_arn    = module.role.role_arn
}
