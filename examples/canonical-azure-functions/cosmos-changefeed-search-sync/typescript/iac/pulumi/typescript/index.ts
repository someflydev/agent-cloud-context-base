import * as azure from "@pulumi/azure-native";
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config("accb");
const environment = pulumi.getStack() || config.require("environment");
const namePrefix = config.require("namePrefix");

const resourceGroup = new azure.resources.ResourceGroup(`${namePrefix}-${environment}`, {
  resourceGroupName: `${namePrefix}-${environment}`,
  location: "eastus"
});

export const resourceGroupName = resourceGroup.name;
