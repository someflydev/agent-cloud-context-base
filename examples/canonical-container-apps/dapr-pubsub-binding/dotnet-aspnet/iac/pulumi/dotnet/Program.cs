using Pulumi;
using Pulumi.AzureNative.App;
using Pulumi.AzureNative.App.Inputs;
using Pulumi.AzureNative.ContainerRegistry;
using Pulumi.AzureNative.ContainerRegistry.Inputs;
using Pulumi.AzureNative.DocumentDB;
using Pulumi.AzureNative.DocumentDB.Inputs;
using Pulumi.AzureNative.KeyVault;
using Pulumi.AzureNative.KeyVault.Inputs;
using Pulumi.AzureNative.ManagedIdentity;
using Pulumi.AzureNative.OperationalInsights;
using Pulumi.AzureNative.OperationalInsights.Inputs;
using Pulumi.AzureNative.Resources;
using Pulumi.AzureNative.ServiceBus;
using Pulumi.AzureNative.ServiceBus.Inputs;

return await Deployment.RunAsync(() =>
{
    var config = new Config("accb");
    var environment = config.Require("environment");
    var location = config.Get("location") ?? "eastus";
    var image = config.Get("image") ?? $"accb{environment}acr.azurecr.io/aca-dapr:latest";
    var stackName = Deployment.Instance.StackName;
    var namePrefix = $"accb-{environment}-aca-dapr";
    var tags = new InputMap<string>
    {
        ["ManagedBy"] = "accb",
        ["Environment"] = environment,
        ["StackName"] = stackName,
        ["Family"] = "canonical-container-apps"
    };

    var group = new ResourceGroup("main", new ResourceGroupArgs
    {
        ResourceGroupName = $"{namePrefix}-rg",
        Location = location,
        Tags = tags
    });

    var identity = new UserAssignedIdentity("aca", new UserAssignedIdentityArgs
    {
        ResourceGroupName = group.Name,
        ResourceName = $"{namePrefix}-mi",
        Location = group.Location,
        Tags = tags
    });

    var logs = new Workspace("logs", new WorkspaceArgs
    {
        ResourceGroupName = group.Name,
        WorkspaceName = $"{namePrefix}-logs",
        Location = group.Location,
        Sku = new WorkspaceSkuArgs { Name = "PerGB2018" },
        RetentionInDays = 30,
        Tags = tags
    });

    var env = new ManagedEnvironment("env", new ManagedEnvironmentArgs
    {
        ResourceGroupName = group.Name,
        EnvironmentName = $"{namePrefix}-env",
        Location = group.Location,
        Tags = tags
    });

    var acr = new Registry("acr", new RegistryArgs
    {
        RegistryName = $"accb{environment}acadapracr",
        ResourceGroupName = group.Name,
        Location = group.Location,
        Sku = new SkuArgs { Name = "Basic" },
        AdminUserEnabled = false,
        Tags = tags
    });

    var bus = new Namespace("events", new NamespaceArgs
    {
        NamespaceName = $"{namePrefix}-sb",
        ResourceGroupName = group.Name,
        Location = group.Location,
        Sku = new SBSkuArgs { Name = "Standard", Tier = "Standard" },
        Tags = tags
    });

    var topic = new Topic("orders", new TopicArgs
    {
        TopicName = "orders",
        NamespaceName = bus.Name,
        ResourceGroupName = group.Name
    });

    var cosmos = new DatabaseAccount("state", new DatabaseAccountArgs
    {
        AccountName = $"{namePrefix}-cosmos",
        ResourceGroupName = group.Name,
        Location = group.Location,
        DatabaseAccountOfferType = "Standard",
        Locations = new[] { new LocationArgs { LocationName = group.Location, FailoverPriority = 0 } },
        ConsistencyPolicy = new ConsistencyPolicyArgs { DefaultConsistencyLevel = "Session" },
        Tags = tags
    });

    var vault = new Vault("secrets", new VaultArgs
    {
        VaultName = $"{namePrefix}-kv",
        ResourceGroupName = group.Name,
        Location = group.Location,
        Properties = new VaultPropertiesArgs
        {
            TenantId = identity.TenantId,
            Sku = new Pulumi.AzureNative.KeyVault.Inputs.SkuArgs { Family = "A", Name = "standard" }
        },
        Tags = tags
    });

    var pubsub = new ManagedEnvironmentsDaprComponent("pubsub", new ManagedEnvironmentsDaprComponentArgs
    {
        ComponentName = "servicebus-pubsub",
        EnvironmentName = env.Name,
        ResourceGroupName = group.Name,
        ComponentType = "pubsub.azure.servicebus.topics",
        Version = "v1",
        Scopes = new[] { "publisher", "subscriber" },
        Metadata = new[] { new DaprMetadataArgs { Name = "namespaceName", Value = bus.Name } }
    });

    var state = new ManagedEnvironmentsDaprComponent("state", new ManagedEnvironmentsDaprComponentArgs
    {
        ComponentName = "cosmos-state",
        EnvironmentName = env.Name,
        ResourceGroupName = group.Name,
        ComponentType = "state.azure.cosmosdb",
        Version = "v1",
        Scopes = new[] { "publisher", "subscriber" },
        Metadata = new[] { new DaprMetadataArgs { Name = "database", Value = "workflow" } }
    });

    var secretStore = new ManagedEnvironmentsDaprComponent("secrets", new ManagedEnvironmentsDaprComponentArgs
    {
        ComponentName = "keyvault-secrets",
        EnvironmentName = env.Name,
        ResourceGroupName = group.Name,
        ComponentType = "secretstores.azure.keyvault",
        Version = "v1",
        Scopes = new[] { "publisher", "subscriber" },
        Metadata = new[] { new DaprMetadataArgs { Name = "vaultName", Value = vault.Name } }
    });

    ContainerApp MakeApp(string logicalName, string appId, bool external)
    {
        return new ContainerApp(logicalName, new ContainerAppArgs
        {
            ContainerAppName = $"{namePrefix}-{appId}",
            ResourceGroupName = group.Name,
            ManagedEnvironmentId = env.Id,
            Location = group.Location,
            Identity = new ManagedServiceIdentityArgs
            {
                Type = "UserAssigned",
                UserAssignedIdentities = identity.Id.Apply(id => new InputMap<UserAssignedIdentityArgs> { [id] = new UserAssignedIdentityArgs() })
            },
            Configuration = new ConfigurationArgs
            {
                Ingress = new IngressArgs { External = external, TargetPort = 8080 }
            },
            Dapr = new DaprArgs { AppId = appId, AppPort = 8080 },
            Template = new TemplateArgs
            {
                Containers = new[]
                {
                    new ContainerArgs
                    {
                        Name = appId,
                        Image = image,
                        Resources = new ContainerResourcesArgs { Cpu = 0.5, Memory = "1Gi" }
                    }
                },
                Scale = new ScaleArgs { MinReplicas = external ? 1 : 0, MaxReplicas = external ? 3 : 5 }
            },
            Tags = tags
        });
    }

    var publisher = MakeApp("publisher", "publisher", true);
    var subscriber = MakeApp("subscriber", "subscriber", false);

    return new Dictionary<string, object?>
    {
        ["publisherName"] = publisher.Name,
        ["subscriberName"] = subscriber.Name,
        ["serviceBusTopic"] = topic.Name,
        ["cosmosAccount"] = cosmos.Name,
        ["keyVaultName"] = vault.Name,
        ["managedIdentityId"] = identity.Id,
        ["acrLoginServer"] = acr.LoginServer,
        ["logWorkspace"] = logs.Name,
        ["daprComponents"] = new[] { pubsub.Name, state.Name, secretStore.Name }
    };
});
