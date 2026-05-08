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
using Pulumi.AzureNative.Storage;
using Pulumi.AzureNative.Storage.Inputs;

return await Deployment.RunAsync(() =>
{
    var config = new Config("accb");
    var environment = config.Require("environment");
    var location = config.Get("location") ?? "eastus";
    var image = config.Get("image") ?? $"accb{environment}acr.azurecr.io/aca-public-worker-dotnet:latest";
    var stackName = Deployment.Instance.StackName;
    var namePrefix = $"accb-{environment}-aca-public-worker-dotnet";
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
        AppLogsConfiguration = new AppLogsConfigurationArgs
        {
            Destination = "log-analytics",
            LogAnalyticsConfiguration = new LogAnalyticsConfigurationArgs
            {
                CustomerId = logs.CustomerId,
                SharedKey = logs.SharedKeys.Apply(keys => keys.PrimarySharedKey)
            }
        },
        Tags = tags
    });

    var acr = new Registry("acr", new RegistryArgs
    {
        RegistryName = $"accb{environment}acapublicdotnetacr",
        ResourceGroupName = group.Name,
        Location = group.Location,
        Sku = new Pulumi.AzureNative.ContainerRegistry.Inputs.SkuArgs { Name = "Basic" },
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

    var queue = new Pulumi.AzureNative.ServiceBus.Queue("work", new QueueArgs
    {
        QueueName = $"{namePrefix}-work",
        NamespaceName = bus.Name,
        ResourceGroupName = group.Name
    });

    var cosmos = new DatabaseAccount("state", new DatabaseAccountArgs
    {
        AccountName = $"{namePrefix}-cosmos",
        ResourceGroupName = group.Name,
        Location = group.Location,
        DatabaseAccountOfferType = "Standard",
        Kind = "GlobalDocumentDB",
        Locations = new[] { new Pulumi.AzureNative.DocumentDB.Inputs.LocationArgs { LocationName = group.Location, FailoverPriority = 0 } },
        ConsistencyPolicy = new ConsistencyPolicyArgs { DefaultConsistencyLevel = "Session" },
        Tags = tags
    });

    var attachments = new StorageAccount("attachments", new StorageAccountArgs
    {
        AccountName = $"accb{environment}acapublicdotnetblob",
        ResourceGroupName = group.Name,
        Location = group.Location,
        Sku = new Pulumi.AzureNative.Storage.Inputs.SkuArgs { Name = Pulumi.AzureNative.Storage.SkuName.Standard_LRS },
        Kind = Pulumi.AzureNative.Storage.Kind.StorageV2,
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

    var publicApi = new ContainerApp("public-api", new ContainerAppArgs
    {
        ContainerAppName = $"{namePrefix}-api",
        ResourceGroupName = group.Name,
        ManagedEnvironmentId = env.Id,
        Location = group.Location,
        Configuration = new ConfigurationArgs
        {
            Ingress = new IngressArgs { External = true, TargetPort = 8080 },
            Secrets = new[]
            {
                new SecretArgs
                {
                    Name = "api-key",
                    KeyVaultUrl = vault.Properties.Apply(properties => $"{properties.VaultUri}secrets/api-key"),
                    Identity = identity.Id
                }
            }
        },
        Identity = new ManagedServiceIdentityArgs
        {
            Type = "UserAssigned",
            UserAssignedIdentities = identity.Id.Apply(id => new InputMap<UserAssignedIdentityArgs> { [id] = new UserAssignedIdentityArgs() })
        },
        Template = new TemplateArgs
        {
            Containers = new[]
            {
                new ContainerArgs
                {
                    Name = "api",
                    Image = image,
                    Env = new[]
                    {
                        new EnvironmentVarArgs { Name = "SERVICEBUS_QUEUE", Value = queue.Name },
                        new EnvironmentVarArgs { Name = "API_SECRET_NAME", SecretRef = "api-key" }
                    },
                    Resources = new ContainerResourcesArgs { Cpu = 0.5, Memory = "1Gi" }
                }
            },
            Scale = new ScaleArgs { MinReplicas = 1, MaxReplicas = 5 }
        },
        Tags = tags
    });

    var privateWorker = new ContainerApp("private-worker", new ContainerAppArgs
    {
        ContainerAppName = $"{namePrefix}-worker",
        ResourceGroupName = group.Name,
        ManagedEnvironmentId = env.Id,
        Location = group.Location,
        Configuration = new ConfigurationArgs
        {
            Ingress = new IngressArgs { External = false, TargetPort = 8080 }
        },
        Identity = new ManagedServiceIdentityArgs
        {
            Type = "UserAssigned",
            UserAssignedIdentities = identity.Id.Apply(id => new InputMap<UserAssignedIdentityArgs> { [id] = new UserAssignedIdentityArgs() })
        },
        Template = new TemplateArgs
        {
            Containers = new[]
            {
                new ContainerArgs
                {
                    Name = "worker",
                    Image = image,
                    Resources = new ContainerResourcesArgs { Cpu = 0.5, Memory = "1Gi" }
                }
            },
            Scale = new ScaleArgs
            {
                MinReplicas = 0,
                MaxReplicas = 10,
                Rules = new[]
                {
                    new ScaleRuleArgs
                    {
                        Name = "servicebus-depth",
                        Custom = new CustomScaleRuleArgs
                        {
                            Type = "azure-servicebus",
                            Metadata = new InputMap<string>
                            {
                                { "queueName", queue.Name },
                                { "namespace", bus.Name },
                                { "messageCount", "5" }
                            }
                        }
                    }
                }
            }
        },
        Tags = tags
    });

    var retryJob = new Job("retry-job", new JobArgs
    {
        JobName = $"{namePrefix}-retry",
        ResourceGroupName = group.Name,
        ManagedEnvironmentId = env.Id,
        Location = group.Location,
        Configuration = new JobConfigurationArgs
        {
            TriggerType = "Event",
            ReplicaTimeout = 300,
            ReplicaRetryLimit = 1,
            EventTriggerConfig = new JobConfigurationEventTriggerConfigArgs
            {
                Parallelism = 1,
                ReplicaCompletionCount = 1,
                Scale = new JobScaleArgs
                {
                    MinExecutions = 0,
                    MaxExecutions = 5,
                    Rules = new[]
                    {
                        new JobScaleRuleArgs
                        {
                            Name = "servicebus-retry",
                            Type = "azure-servicebus",
                            Metadata = new InputMap<string>
                            {
                                { "queueName", queue.Name },
                                { "namespace", bus.Name },
                                { "messageCount", "5" }
                            }
                        }
                    }
                }
            }
        },
        Template = new JobTemplateArgs
        {
            Containers = new[]
            {
                new ContainerArgs
                {
                    Name = "retry",
                    Image = image,
                    Args = new[] { "/retry" },
                    Resources = new ContainerResourcesArgs { Cpu = 0.5, Memory = "1Gi" }
                }
            }
        },
        Tags = tags
    });

    return new Dictionary<string, object?>
    {
        ["publicApiUrl"] = publicApi.Configuration.Apply(cfg => cfg.Ingress.Fqdn),
        ["privateWorkerName"] = privateWorker.Name,
        ["retryJobName"] = retryJob.Name,
        ["serviceBusQueue"] = queue.Name,
        ["cosmosAccount"] = cosmos.Name,
        ["attachmentAccount"] = attachments.Name,
        ["keyVaultUri"] = vault.Properties.Apply(properties => properties.VaultUri),
        ["managedIdentityId"] = identity.Id,
        ["acrLoginServer"] = acr.LoginServer,
        ["logWorkspace"] = logs.Name
    };
});
