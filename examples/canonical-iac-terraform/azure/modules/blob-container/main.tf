variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "location" { type = string }

resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-${var.environment}-storage-rg"
  location = var.location
}

resource "azurerm_storage_account" "this" {
  name                     = replace("${var.name_prefix}${var.environment}st", "-", "")
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "this" {
  name                  = "${var.name_prefix}-${var.environment}-artifacts"
  storage_account_name  = azurerm_storage_account.this.name
  container_access_type = "private"
}

output "storage_account_name" { value = azurerm_storage_account.this.name }
