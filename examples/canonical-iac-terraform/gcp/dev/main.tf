module "bucket" {
  source      = "../modules/gcs-bucket"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "database" {
  source      = "../modules/firestore-database"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "topic" {
  source      = "../modules/pubsub-topic-with-dlq"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "secret" {
  source      = "../modules/secret-manager-secret"
  environment = var.environment
  name_prefix = var.name_prefix
}

module "identity" {
  source      = "../modules/service-account-least-privilege"
  environment = var.environment
  name_prefix = var.name_prefix
  bucket_name = module.bucket.bucket_name
  topic_name  = module.topic.topic_name
  secret_id   = module.secret.secret_id
}

module "function" {
  source        = "../modules/cloudfunction2"
  environment   = var.environment
  name_prefix   = var.name_prefix
  service_email = module.identity.email
}
