import pulumi

from components.eventing_component import EventingComponent
from components.function_component import FunctionComponent
from components.identity_component import IdentityComponent
from components.secret_component import SecretComponent
from components.storage_component import StorageComponent

stack = pulumi.get_stack()
config = pulumi.Config("accb")
environment = config.get("environment") or stack
name_prefix = config.get("namePrefix") or f"accb-{stack}"

storage = StorageComponent(f"{name_prefix}-{environment}-storage", environment=environment, name_prefix=name_prefix)
eventing = EventingComponent(f"{name_prefix}-{environment}-eventing", environment=environment, name_prefix=name_prefix)
secret = SecretComponent(f"{name_prefix}-{environment}-secret", environment=environment, name_prefix=name_prefix)
identity = IdentityComponent(f"{name_prefix}-{environment}-identity", environment=environment, name_prefix=name_prefix)
FunctionComponent(f"{name_prefix}-{environment}-function", environment=environment, name_prefix=name_prefix, service_account=identity.email)

pulumi.export("stackName", stack)
pulumi.export("bucketName", storage.bucket_name)
pulumi.export("topicName", eventing.topic_name)
pulumi.export("secretId", secret.secret_id)
