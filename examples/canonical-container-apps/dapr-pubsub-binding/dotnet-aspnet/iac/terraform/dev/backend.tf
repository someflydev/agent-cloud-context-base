terraform {
  backend "azurerm" {
    resource_group_name  = "accb-dev-tfstate-rg"
    storage_account_name = "accbdevtfstate"
    container_name       = "tfstate"
    key                  = "dev/canonical-container-apps/dapr-pubsub-binding.tfstate"
  }
}
