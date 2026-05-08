import pulumi
import pulumi_azure_native as azure_native

config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = config.require("namePrefix")

resource_group = azure_native.resources.ResourceGroup(
    f"{name_prefix}-{environment}",
    resource_group_name=f"{name_prefix}-{environment}",
    location="eastus",
)

pulumi.export("resource_group_name", resource_group.name)
