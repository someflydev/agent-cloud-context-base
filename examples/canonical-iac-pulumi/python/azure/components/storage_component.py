import pulumi


class StorageComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:azure:StorageComponent", name, None, opts)
        stack = pulumi.get_stack()
        self.storage_name = pulumi.Output.from_input(f"{name_prefix}-{environment}-{stack}-artifacts")
        self.register_outputs({"storage_name": self.storage_name})
