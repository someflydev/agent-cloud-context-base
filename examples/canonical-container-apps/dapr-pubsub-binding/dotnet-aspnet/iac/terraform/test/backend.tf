terraform {
  backend "azurerm" {
    resource_group_name  = "accb-test-tfstate-rg"
    storage_account_name = "accbtesttfstate"
    container_name       = "tfstate"
    key                  = "test/canonical-container-apps/dapr-pubsub-binding.tfstate"
  }
}
