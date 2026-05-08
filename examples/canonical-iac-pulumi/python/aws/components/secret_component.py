import pulumi


class SecretComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:aws:SecretComponent", name, None, opts)
        stack = pulumi.get_stack()
        self.secret_ref = pulumi.Output.from_input(f"{name_prefix}-{environment}-{stack}-config")
        self.register_outputs({"secret_ref": self.secret_ref})
