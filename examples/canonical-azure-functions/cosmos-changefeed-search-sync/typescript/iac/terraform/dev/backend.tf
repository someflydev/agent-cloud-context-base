terraform {
  backend "azurerm" {
    key = "accb/azure-functions/cosmos-search-sync/dev.tfstate"
  }
}
