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
  default = "accbdevacr.azurecr.io/aca-dapr:latest"
}

provider "azurerm" {
  features {}
}

locals {
  name_prefix = "accb-${var.environment}-aca-dapr"
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

resource "azurerm_servicebus_topic" "orders" {
  name         = "orders"
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

resource "azurerm_key_vault" "secrets" {
  name                = "${local.name_prefix}-kv"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = azurerm_user_assigned_identity.aca.tenant_id
  sku_name            = "standard"
  tags                = local.tags
}

resource "azurerm_container_app_environment_dapr_component" "pubsub" {
  name                         = "servicebus-pubsub"
  container_app_environment_id = azurerm_container_app_environment.env.id
  component_type               = "pubsub.azure.servicebus.topics"
  version                      = "v1"
  scopes                       = ["publisher", "subscriber"]

  metadata {
    name  = "namespaceName"
    value = azurerm_servicebus_namespace.events.name
  }
}

resource "azurerm_container_app_environment_dapr_component" "state" {
  name                         = "cosmos-state"
  container_app_environment_id = azurerm_container_app_environment.env.id
  component_type               = "state.azure.cosmosdb"
  version                      = "v1"
  scopes                       = ["publisher", "subscriber"]

  metadata {
    name  = "database"
    value = "workflow"
  }
}

resource "azurerm_container_app_environment_dapr_component" "secrets" {
  name                         = "keyvault-secrets"
  container_app_environment_id = azurerm_container_app_environment.env.id
  component_type               = "secretstores.azure.keyvault"
  version                      = "v1"
  scopes                       = ["publisher", "subscriber"]

  metadata {
    name  = "vaultName"
    value = azurerm_key_vault.secrets.name
  }
}

resource "azurerm_container_app" "publisher" {
  name                         = "${local.name_prefix}-publisher"
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

  dapr {
    app_id   = "publisher"
    app_port = 8080
  }

  template {
    min_replicas = 1
    max_replicas = 3
    container {
      name   = "publisher"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
    }
  }
}

resource "azurerm_container_app" "subscriber" {
  name                         = "${local.name_prefix}-subscriber"
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

  dapr {
    app_id   = "subscriber"
    app_port = 8080
  }

  template {
    min_replicas = 0
    max_replicas = 5
    container {
      name   = "subscriber"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
    }
  }
}
