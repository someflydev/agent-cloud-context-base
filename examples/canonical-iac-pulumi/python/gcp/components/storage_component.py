import pulumi
import pulumi_gcp as gcp


class StorageComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:gcp:StorageComponent", name, None, opts)
        stack = pulumi.get_stack()
        bucket = gcp.storage.Bucket(f"{name_prefix}-{environment}-{stack}-artifacts", location="US", opts=pulumi.ResourceOptions(parent=self))
        self.bucket_name = bucket.name
        self.register_outputs({"bucket_name": self.bucket_name})
