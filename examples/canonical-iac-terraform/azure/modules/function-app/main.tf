variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "location" { type = string }
variable "identity_id" { type = string }

resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-${var.environment}-func-rg"
  location = var.location
}

resource "azurerm_service_plan" "this" {
  name                = "${var.name_prefix}-${var.environment}-plan"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  os_type             = "Linux"
  sku_name            = "Y1"
}
