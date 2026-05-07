import pulumi
from pulumi_gcp import pubsub, serviceaccount

config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-gcp-translation"
labels = {"managed_by": "accb", "environment": environment, "family": "canonical-gcp-functions"}

function_sa = serviceaccount.Account(
    "function",
    account_id=f"{name_prefix}-fn",
    display_name=f"accb {environment} Pub/Sub translation function",
)

source = pubsub.Topic("source", name=f"{name_prefix}-source", labels=labels)
completion = pubsub.Topic("completion", name=f"{name_prefix}-complete", labels=labels)

pulumi.export("service_account_email", function_sa.email)
pulumi.export("source_topic", source.name)
pulumi.export("completion_topic", completion.name)
