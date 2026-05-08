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

storage = StorageComponent(f"{name_prefix}-{environment}-storage", environment, name_prefix)
eventing = EventingComponent(f"{name_prefix}-{environment}-eventing", environment, name_prefix)
secret = SecretComponent(f"{name_prefix}-{environment}-secret", environment, name_prefix)
identity = IdentityComponent(f"{name_prefix}-{environment}-identity", environment, name_prefix, storage.storage_name, eventing.eventing_name, secret.secret_ref)
FunctionComponent(f"{name_prefix}-{environment}-function", environment, name_prefix, identity.identity_ref)

pulumi.export("stack_name", stack)
