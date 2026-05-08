import pulumi


class FunctionComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, identity_ref, opts=None):
        super().__init__("accb:aws:FunctionComponent", name, None, opts)
        stack = pulumi.get_stack()
        self.function_name = pulumi.Output.from_input(f"{name_prefix}-{environment}-{stack}-handler")
        self.register_outputs({"function_name": self.function_name})
