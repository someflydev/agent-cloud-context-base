import pulumi
from pulumi_gcp import pubsub, serviceaccount, storage

config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-gcp-ocr"
labels = {"managed_by": "accb", "environment": environment, "family": "canonical-gcp-functions"}

function_sa = serviceaccount.Account(
    "function",
    account_id=f"{name_prefix}-fn",
    display_name=f"accb {environment} OCR function",
)

input_bucket = storage.Bucket(
    "input",
    name=f"{name_prefix}-input",
    location="US",
    uniform_bucket_level_access=True,
    labels=labels,
)

downstream = pubsub.Topic("downstream", name=f"{name_prefix}-downstream", labels=labels)

pulumi.export("service_account_email", function_sa.email)
pulumi.export("input_bucket", input_bucket.name)
pulumi.export("downstream_topic", downstream.name)
