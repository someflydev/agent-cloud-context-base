using Pulumi;
using Pulumi.AzureNative.ManagedIdentity;

public sealed class IdentityComponent : ComponentResource
{
    public Output<string> IdentityId { get; private set; }

    public IdentityComponent(string name, string environment, string namePrefix, ComponentResourceOptions? opts = null)
        : base("accb:azure:IdentityComponent", name, opts)
    {
        var stackName = Deployment.Instance.StackName;
        var identity = new UserAssignedIdentity($"{namePrefix}-{environment}-{stackName}-identity", new(), new CustomResourceOptions { Parent = this });
        IdentityId = identity.Id;
        RegisterOutputs(new Dictionary<string, object?> { ["identityId"] = IdentityId });
    }
}
