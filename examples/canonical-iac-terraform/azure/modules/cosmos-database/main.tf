variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "location" { type = string }

resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-${var.environment}-cosmos-rg"
  location = var.location
}

resource "azurerm_cosmosdb_account" "this" {
  name                = "${var.name_prefix}-${var.environment}-cosmos"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  offer_type          = "Standard"
  consistency_policy {
    consistency_level = "Session"
  }
  geo_location {
    location          = azurerm_resource_group.this.location
    failover_priority = 0
  }
}
