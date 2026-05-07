import pulumi
import pulumi_gcp as gcp


class SecretComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:gcp:SecretComponent", name, None, opts)
        stack = pulumi.get_stack()
        secret = gcp.secretmanager.Secret(
            f"{name_prefix}-{environment}-{stack}-config",
            secret_id=f"{name_prefix}-{environment}-{stack}-config",
            replication=gcp.secretmanager.SecretReplicationArgs(auto={}),
            opts=pulumi.ResourceOptions(parent=self),
        )
        self.secret_id = secret.secret_id
        self.register_outputs({"secret_id": self.secret_id})
