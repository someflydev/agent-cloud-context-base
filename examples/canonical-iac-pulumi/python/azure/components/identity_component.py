import pulumi


class IdentityComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, storage_name, eventing_name, secret_ref, opts=None):
        super().__init__("accb:azure:IdentityComponent", name, None, opts)
        stack = pulumi.get_stack()
        self.identity_ref = pulumi.Output.from_input(f"{name_prefix}-{environment}-{stack}-runtime")
        self.register_outputs({"identity_ref": self.identity_ref})
