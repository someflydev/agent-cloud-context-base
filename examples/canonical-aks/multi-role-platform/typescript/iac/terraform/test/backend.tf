terraform {
  backend "azurerm" {
    resource_group_name  = "accb-tfstate-test"
    storage_account_name = "accbtfstatetest"
    container_name       = "tfstate"
    key                  = "canonical-aks/test.tfstate"
  }
}
