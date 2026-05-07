using Pulumi;
using Pulumi.AzureNative.KeyVault;

public sealed class SecretComponent : ComponentResource
{
    public Output<string> SecretName { get; private set; }

    public SecretComponent(string name, string environment, string namePrefix, ComponentResourceOptions? opts = null)
        : base("accb:azure:SecretComponent", name, opts)
    {
        var stackName = Deployment.Instance.StackName;
        var vault = new Vault($"{namePrefix}-{environment}-{stackName}-kv", new(), new CustomResourceOptions { Parent = this });
        SecretName = vault.Name.Apply(v => $"{v}-{environment}-config");
        RegisterOutputs(new Dictionary<string, object?> { ["secretName"] = SecretName });
    }
}
