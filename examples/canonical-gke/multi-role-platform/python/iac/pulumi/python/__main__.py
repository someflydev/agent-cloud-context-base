import pulumi

env = pulumi.get_stack()
name = f"accb-gcp-{env}-multi-role-platform"
secret_path = f"projects/accb/secrets/gke-multi-role-platform/{env}/workload"

pulumi.export("cluster_name", name)
pulumi.export("secret_path", secret_path)
