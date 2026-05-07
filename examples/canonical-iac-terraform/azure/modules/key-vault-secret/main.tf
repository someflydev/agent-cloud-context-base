variable "environment" { type = string }
variable "name_prefix" { type = string }
variable "location" { type = string }

resource "azurerm_resource_group" "this" {
  name     = "${var.name_prefix}-${var.environment}-kv-rg"
  location = var.location
}

resource "azurerm_key_vault" "this" {
  name                = replace("${var.name_prefix}-${var.environment}-kv", "-", "")
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  tenant_id           = "00000000-0000-0000-0000-000000000000"
  sku_name            = "standard"
}

resource "azurerm_key_vault_secret" "placeholder" {
  name         = "${var.name_prefix}-${var.environment}-config-ref"
  value        = "set-by-operator"
  key_vault_id = azurerm_key_vault.this.id
}
