import pulumi
from pulumi_gcp import pubsub, serviceaccount

config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-gcp-firebase-onboarding"
labels = {"managed_by": "accb", "environment": environment, "family": "canonical-gcp-functions"}

function_sa = serviceaccount.Account(
    "function",
    account_id=f"{name_prefix}-fn",
    display_name=f"accb {environment} Firebase onboarding function",
)

onboarding = pubsub.Topic("onboarding", name=f"{name_prefix}-events", labels=labels)

pulumi.export("service_account_email", function_sa.email)
pulumi.export("onboarding_topic", onboarding.name)
