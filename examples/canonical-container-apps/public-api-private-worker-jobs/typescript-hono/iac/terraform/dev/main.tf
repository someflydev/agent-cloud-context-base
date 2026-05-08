terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.110" }
  }
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "image" {
  type    = string
  default = "accbdevacr.azurecr.io/aca-public-worker-typescript:latest"
}

provider "azurerm" {
  features {}
}

locals {
  name_prefix = "accb-${var.environment}-aca-public-worker-typescript"
  tags        = { ManagedBy = "accb", Environment = var.environment, Family = "canonical-container-apps" }
}

resource "azurerm_resource_group" "main" {
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.tags
}

resource "azurerm_user_assigned_identity" "aca" {
  name                = "${local.name_prefix}-mi"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.tags
}

resource "azurerm_log_analytics_workspace" "logs" {
  name                = "${local.name_prefix}-logs"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.tags
}

resource "azurerm_container_app_environment" "env" {
  name                       = "${local.name_prefix}-env"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
  tags                       = local.tags
}

resource "azurerm_container_registry" "acr" {
  name                = replace("${local.name_prefix}acr", "-", "")
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = local.tags
}

resource "azurerm_servicebus_namespace" "events" {
  name                = "${local.name_prefix}-sb"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  tags                = local.tags
}

resource "azurerm_servicebus_queue" "work" {
  name         = "${local.name_prefix}-work"
  namespace_id = azurerm_servicebus_namespace.events.id
}

resource "azurerm_cosmosdb_account" "state" {
  name                = "${local.name_prefix}-cosmos"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  consistency_policy {
    consistency_level = "Session"
  }
  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
  tags = local.tags
}

resource "azurerm_storage_account" "attachments" {
  name                     = replace("${local.name_prefix}blob", "-", "")
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = local.tags
}

resource "azurerm_key_vault" "secrets" {
  name                = "${local.name_prefix}-kv"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = azurerm_user_assigned_identity.aca.tenant_id
  sku_name            = "standard"
  tags                = local.tags
}

resource "azurerm_container_app" "public_api" {
  name                         = "${local.name_prefix}-api"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"
  tags                         = local.tags

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aca.id]
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  secret {
    name                = "api-key"
    key_vault_secret_id = "${azurerm_key_vault.secrets.vault_uri}secrets/api-key"
    identity            = azurerm_user_assigned_identity.aca.id
  }

  template {
    min_replicas = 1
    max_replicas = 5
    container {
      name   = "api"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
      env {
        name  = "SERVICEBUS_QUEUE"
        value = azurerm_servicebus_queue.work.name
      }
      env {
        name        = "API_SECRET_NAME"
        secret_name = "api-key"
      }
    }
  }
}

resource "azurerm_container_app" "private_worker" {
  name                         = "${local.name_prefix}-worker"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"
  tags                         = local.tags

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aca.id]
  }

  ingress {
    external_enabled = false
    target_port      = 8080
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 10
    custom_scale_rule {
      name             = "servicebus-depth"
      custom_rule_type = "azure-servicebus"
      metadata = {
        queueName   = azurerm_servicebus_queue.work.name
        namespace   = azurerm_servicebus_namespace.events.name
        messageCount = "5"
      }
    }
    container {
      name   = "worker"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
    }
  }
}

resource "azurerm_container_app_job" "retry" {
  name                         = "${local.name_prefix}-retry"
  location                     = azurerm_resource_group.main.location
  resource_group_name          = azurerm_resource_group.main.name
  container_app_environment_id = azurerm_container_app_environment.env.id
  replica_timeout_in_seconds   = 300
  replica_retry_limit          = 1
  tags                         = local.tags

  event_trigger_config {
    parallelism              = 1
    replica_completion_count = 1
    scale {
      min_executions              = 0
      max_executions              = 5
      polling_interval_in_seconds = 30
      rules {
        name = "servicebus-retry"
        type = "azure-servicebus"
        metadata = {
          queueName    = azurerm_servicebus_queue.work.name
          namespace    = azurerm_servicebus_namespace.events.name
          messageCount = "5"
        }
      }
    }
  }

  template {
    container {
      name   = "retry"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
      args   = ["/retry"]
    }
  }
}
