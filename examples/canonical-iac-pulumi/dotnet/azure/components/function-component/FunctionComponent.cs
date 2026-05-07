using Pulumi;
using Pulumi.AzureNative.Web;

public sealed class FunctionComponent : ComponentResource
{
    public FunctionComponent(string name, string environment, string namePrefix, Input<string> identityId, ComponentResourceOptions? opts = null)
        : base("accb:azure:FunctionComponent", name, opts)
    {
        var stackName = Deployment.Instance.StackName;
        _ = new WebApp($"{namePrefix}-{environment}-{stackName}-func", new WebAppArgs
        {
            Kind = "functionapp,linux"
        }, new CustomResourceOptions { Parent = this });
        RegisterOutputs();
    }
}
