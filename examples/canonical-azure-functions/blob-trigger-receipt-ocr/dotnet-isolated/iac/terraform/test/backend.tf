terraform {
  backend "azurerm" {
    key = "accb/azure-functions/blob-trigger-receipt-ocr/test.tfstate"
  }
}
