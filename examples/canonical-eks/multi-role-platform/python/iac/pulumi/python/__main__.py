import pulumi

env = pulumi.get_stack()
name = f"accb-aws-{env}-multi-role-platform"
secret_path = f"/accb/eks/multi-role-platform/{env}/workload"

pulumi.export("cluster_name", name)
pulumi.export("secret_path", secret_path)
