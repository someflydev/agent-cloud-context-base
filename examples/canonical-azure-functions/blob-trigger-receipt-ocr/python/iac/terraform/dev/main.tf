variable "environment" {}
variable "name_prefix" {}
variable "secret_path" {}

resource "azurerm_resource_group" "example" {
  name     = "${var.name_prefix}-${var.environment}"
  location = "eastus"
}
