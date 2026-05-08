using Pulumi;
using AzureNative = Pulumi.AzureNative;

return await Deployment.RunAsync(() =>
{
    var config = new Config("accb");
    var environment = config.Require("environment");
    var namePrefix = config.Require("namePrefix");
    var resourceGroup = new AzureNative.Resources.ResourceGroup($"{namePrefix}-{environment}", new()
    {
        ResourceGroupName = $"{namePrefix}-{environment}",
        Location = "eastus"
    });
    return new Dictionary<string, object?> { ["resourceGroupName"] = resourceGroup.Name };
});
