terraform {
  backend "azurerm" {
    key = "accb/azure-functions/servicebus-classification/dev.tfstate"
  }
}
