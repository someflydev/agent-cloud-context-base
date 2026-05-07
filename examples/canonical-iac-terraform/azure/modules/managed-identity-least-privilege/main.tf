variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "location" { type = string }

resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-${var.environment}-rg"
  location = var.location
}

resource "azurerm_user_assigned_identity" "this" {
  name                = "${var.name_prefix}-${var.environment}-identity"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
}

output "identity_id" { value = azurerm_user_assigned_identity.this.id }
output "resource_group_name" { value = azurerm_resource_group.this.name }
