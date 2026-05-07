using Pulumi;

return await Deployment.RunAsync(() =>
{
    var env = Deployment.Instance.StackName;
    var name = $"accb-azure-{env}-multi-role-platform";
    var contract = new Pulumi.CustomResource("accb:contract:Cluster", name, new CustomResourceArgs
    {
        { "environment", env },
        { "secretPath", $"https://accb-kv.vault.azure.net/secrets/aks-multi-role-platform/{env}/workload" }
    });
    return new Dictionary<string, object?> { ["clusterName"] = name };
});
