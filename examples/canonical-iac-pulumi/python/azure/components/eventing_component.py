import pulumi


class EventingComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:azure:EventingComponent", name, None, opts)
        stack = pulumi.get_stack()
        self.eventing_name = pulumi.Output.from_input(f"{name_prefix}-{environment}-{stack}-events")
        self.register_outputs({"eventing_name": self.eventing_name})
