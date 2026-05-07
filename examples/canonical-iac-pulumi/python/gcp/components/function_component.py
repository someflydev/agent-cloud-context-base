import pulumi
import pulumi_gcp as gcp


class FunctionComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, service_account, opts=None):
        super().__init__("accb:gcp:FunctionComponent", name, None, opts)
        stack = pulumi.get_stack()
        gcp.cloudfunctionsv2.Function(
            f"{name_prefix}-{environment}-{stack}-handler",
            location="us-central1",
            build_config=gcp.cloudfunctionsv2.FunctionBuildConfigArgs(runtime="python312", entry_point="main"),
            service_config=gcp.cloudfunctionsv2.FunctionServiceConfigArgs(service_account_email=service_account),
            opts=pulumi.ResourceOptions(parent=self),
        )
        self.register_outputs({})
