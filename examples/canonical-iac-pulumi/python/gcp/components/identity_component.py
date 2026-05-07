import pulumi
import pulumi_gcp as gcp


class IdentityComponent(pulumi.ComponentResource):
    def __init__(self, name: str, environment: str, name_prefix: str, opts=None):
        super().__init__("accb:gcp:IdentityComponent", name, None, opts)
        stack = pulumi.get_stack()
        account = gcp.serviceaccount.Account(
            f"{name_prefix}-{environment}-{stack}-runtime",
            account_id=f"{name_prefix}-{environment}-{stack}-runtime",
            display_name=f"accb {environment} runtime",
            opts=pulumi.ResourceOptions(parent=self),
        )
        self.email = account.email
        self.register_outputs({"email": self.email})
