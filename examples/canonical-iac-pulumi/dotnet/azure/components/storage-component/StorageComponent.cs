using Pulumi;
using Pulumi.AzureNative.Storage;

public sealed class StorageComponent : ComponentResource
{
    public Output<string> StorageAccountName { get; private set; }

    public StorageComponent(string name, string environment, string namePrefix, ComponentResourceOptions? opts = null)
        : base("accb:azure:StorageComponent", name, opts)
    {
        var stackName = Deployment.Instance.StackName;
        var account = new StorageAccount($"{namePrefix}-{environment}-{stackName}-st", new StorageAccountArgs
        {
            Kind = Kind.StorageV2,
            Sku = new Pulumi.AzureNative.Storage.Inputs.SkuArgs { Name = SkuName.Standard_LRS }
        }, new CustomResourceOptions { Parent = this });
        StorageAccountName = account.Name;
        RegisterOutputs(new Dictionary<string, object?> { ["storageAccountName"] = StorageAccountName });
    }
}
