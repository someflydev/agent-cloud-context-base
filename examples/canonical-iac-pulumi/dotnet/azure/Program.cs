using Pulumi;

return await Deployment.RunAsync(() =>
{
    var stackName = Deployment.Instance.StackName;
    var config = new Config("accb");
    var environment = config.Get("environment") ?? stackName;
    var namePrefix = config.Get("namePrefix") ?? $"accb-{stackName}";

    var identity = new IdentityComponent($"{namePrefix}-{environment}-identity", environment, namePrefix);
    var storage = new StorageComponent($"{namePrefix}-{environment}-storage", environment, namePrefix);
    var eventing = new EventingComponent($"{namePrefix}-{environment}-eventing", environment, namePrefix);
    var secret = new SecretComponent($"{namePrefix}-{environment}-secret", environment, namePrefix);
    var function = new FunctionComponent($"{namePrefix}-{environment}-function", environment, namePrefix, identity.IdentityId);

    return new Dictionary<string, object?>
    {
        ["stackName"] = stackName,
        ["identityId"] = identity.IdentityId,
        ["storageAccount"] = storage.StorageAccountName,
        ["queueName"] = eventing.QueueName,
        ["secretName"] = secret.SecretName,
    };
});
