terraform {
  backend "azurerm" {
    resource_group_name  = "accb-dev-tfstate-rg"
    storage_account_name = "accbdevtfstate"
    container_name       = "tfstate"
    key                  = "canonical-iac-terraform/azure/dev.tfstate"
  }
}
