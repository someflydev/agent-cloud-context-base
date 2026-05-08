terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.110" }
  }
}

variable "environment" {
  type    = string
  default = "test"
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "image" {
  type    = string
  default = "accbtestacr.azurecr.io/aca-public-worker-dotnet:latest"
}

provider "azurerm" {
  features {}
}

locals {
  name_prefix = "accb-${var.environment}-aca-public-worker-dotnet"
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

  template {
    min_replicas = 1
    max_replicas = 3
    container {
      name   = "api"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
    }
  }
}
