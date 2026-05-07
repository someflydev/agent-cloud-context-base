using Pulumi;
using Pulumi.AzureNative.ServiceBus;

public sealed class EventingComponent : ComponentResource
{
    public Output<string> QueueName { get; private set; }

    public EventingComponent(string name, string environment, string namePrefix, ComponentResourceOptions? opts = null)
        : base("accb:azure:EventingComponent", name, opts)
    {
        var stackName = Deployment.Instance.StackName;
        var queue = new Queue($"{namePrefix}-{environment}-{stackName}-main", new QueueArgs
        {
            MaxDeliveryCount = 5
        }, new CustomResourceOptions { Parent = this });
        QueueName = queue.Name;
        RegisterOutputs(new Dictionary<string, object?> { ["queueName"] = QueueName });
    }
}
