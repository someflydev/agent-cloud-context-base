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
  default = "accbtestacr.azurecr.io/aca-dapr:latest"
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
    max_replicas = 2
    container {
      name   = "publisher"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"
    }
  }
}
