terraform {
  backend "azurerm" {
    resource_group_name  = "accb-tfstate-dev"
    storage_account_name = "accbtfstatedev"
    container_name       = "tfstate"
    key                  = "canonical-aks/dev.tfstate"
  }
}
