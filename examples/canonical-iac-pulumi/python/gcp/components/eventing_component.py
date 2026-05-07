import pulumi
import pulumi_gcp as gcp


class EventingComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:gcp:EventingComponent", name, None, opts)
        stack = pulumi.get_stack()
        dlq = gcp.pubsub.Topic(f"{name_prefix}-{environment}-{stack}-dlq", opts=pulumi.ResourceOptions(parent=self))
        topic = gcp.pubsub.Topic(f"{name_prefix}-{environment}-{stack}-main", opts=pulumi.ResourceOptions(parent=self))
        gcp.pubsub.Subscription(
            f"{name_prefix}-{environment}-{stack}-sub",
            topic=topic.name,
            dead_letter_policy=gcp.pubsub.SubscriptionDeadLetterPolicyArgs(dead_letter_topic=dlq.id, max_delivery_attempts=5),
            opts=pulumi.ResourceOptions(parent=self),
        )
        self.topic_name = topic.name
        self.register_outputs({"topic_name": self.topic_name})
