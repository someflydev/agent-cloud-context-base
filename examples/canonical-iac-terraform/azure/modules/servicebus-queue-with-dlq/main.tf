variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "location" { type = string }

resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-${var.environment}-sb-rg"
  location = var.location
}

resource "azurerm_servicebus_namespace" "this" {
  name                = "${var.name_prefix}-${var.environment}-sb"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku                 = "Standard"
}

resource "azurerm_servicebus_queue" "this" {
  name         = "${var.name_prefix}-${var.environment}-main"
  namespace_id = azurerm_servicebus_namespace.this.id
}

output "queue_name" { value = azurerm_servicebus_queue.this.name }
