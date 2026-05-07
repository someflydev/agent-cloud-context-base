module "identity" {
  source      = "../modules/managed-identity-least-privilege"
  environment = var.environment
  name_prefix = var.name_prefix
  location    = var.location
}

module "blob" {
  source      = "../modules/blob-container"
  environment = var.environment
  name_prefix = var.name_prefix
  location    = var.location
}

module "cosmos" {
  source      = "../modules/cosmos-database"
  environment = var.environment
  name_prefix = var.name_prefix
  location    = var.location
}

module "servicebus" {
  source      = "../modules/servicebus-queue-with-dlq"
  environment = var.environment
  name_prefix = var.name_prefix
  location    = var.location
}

module "secret" {
  source      = "../modules/key-vault-secret"
  environment = var.environment
  name_prefix = var.name_prefix
  location    = var.location
}

module "function" {
  source       = "../modules/function-app"
  environment  = var.environment
  name_prefix  = var.name_prefix
  location     = var.location
  identity_id  = module.identity.identity_id
}
