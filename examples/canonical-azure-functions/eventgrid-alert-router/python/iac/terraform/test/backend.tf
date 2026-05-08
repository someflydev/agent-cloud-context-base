terraform {
  backend "azurerm" {
    key = "accb/azure-functions/eventgrid-alert-router/test.tfstate"
  }
}
