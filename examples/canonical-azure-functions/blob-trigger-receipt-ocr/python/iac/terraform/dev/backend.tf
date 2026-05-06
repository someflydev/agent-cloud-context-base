terraform {
  backend "azurerm" {
    key = "accb/azure-functions/blob-receipt-ocr/dev.tfstate"
  }
}
