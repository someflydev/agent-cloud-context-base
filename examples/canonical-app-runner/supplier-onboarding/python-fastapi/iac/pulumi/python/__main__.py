import json

import pulumi
from pulumi_aws import apprunner, ecr, ec2, iam, rds, secretsmanager


config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-apprunner-vpc"
tags = {"ManagedBy": "accb", "Environment": environment, "Family": "canonical-app-runner"}
subnet_ids = config.get_object("subnet_ids") or [f"subnet-replace-me-{environment}-a", f"subnet-replace-me-{environment}-b"]
vpc_id = config.get("vpc_id") or f"vpc-replace-me-{environment}"

service_role = iam.Role(
    "service",
    name=f"{name_prefix}-service-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "tasks.apprunner.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    ),
    tags=tags,
)

access_role = iam.Role(
    "access",
    name=f"{name_prefix}-access-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "build.apprunner.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    ),
    tags=tags,
)

repo = ecr.Repository(
    "repo",
    name=f"{name_prefix}-repo",
    image_scanning_configuration=ecr.RepositoryImageScanningConfigurationArgs(scan_on_push=True),
    tags=tags,
)

db_secret = secretsmanager.Secret("db", name=f"/accb/{environment}/apprunner/vpc/db", tags=tags)

connector_sg = ec2.SecurityGroup(
    "connector",
    name=f"{name_prefix}-connector",
    description=f"App Runner connector for {environment}",
    vpc_id=vpc_id,
    tags=tags,
)

db_sg = ec2.SecurityGroup(
    "db",
    name=f"{name_prefix}-db",
    description=f"Aurora Postgres for {environment}",
    vpc_id=vpc_id,
    tags=tags,
)

db_subnets = rds.SubnetGroup("db-subnets", name=f"{name_prefix}-db", subnet_ids=subnet_ids, tags=tags)

cluster = rds.Cluster(
    "aurora",
    cluster_identifier=f"{name_prefix}-aurora",
    engine="aurora-postgresql",
    engine_mode="provisioned",
    database_name="app",
    manage_master_user_password=True,
    db_subnet_group_name=db_subnets.name,
    vpc_security_group_ids=[db_sg.id],
    tags=tags,
)

vpc_connector = apprunner.VpcConnector(
    "connector",
    vpc_connector_name=f"{name_prefix}-connector",
    subnets=subnet_ids,
    security_groups=[connector_sg.id],
    tags=tags,
)

service = apprunner.Service(
    "service",
    service_name=f"{name_prefix}-service",
    source_configuration=apprunner.ServiceSourceConfigurationArgs(
        authentication_configuration=apprunner.ServiceSourceConfigurationAuthenticationConfigurationArgs(
            access_role_arn=access_role.arn,
        ),
        auto_deployments_enabled=True,
        image_repository=apprunner.ServiceSourceConfigurationImageRepositoryArgs(
            image_identifier=repo.repository_url.apply(lambda url: f"{url}:test"),
            image_repository_type="ECR",
            image_configuration=apprunner.ServiceSourceConfigurationImageRepositoryImageConfigurationArgs(
                port="8080",
                runtime_environment_variables={
                    "DB_SECRET_PATH": db_secret.name,
                    "DB_HOST": cluster.endpoint,
                },
            ),
        ),
    ),
    instance_configuration=apprunner.ServiceInstanceConfigurationArgs(instance_role_arn=service_role.arn),
    network_configuration=apprunner.ServiceNetworkConfigurationArgs(
        egress_configuration=apprunner.ServiceNetworkConfigurationEgressConfigurationArgs(
            egress_type="VPC",
            vpc_connector_arn=vpc_connector.arn,
        )
    ),
    tags=tags,
)

pulumi.export("service_role_arn", service_role.arn)
pulumi.export("access_role_arn", access_role.arn)
pulumi.export("repository_url", repo.repository_url)
pulumi.export("db_secret_name", db_secret.name)
pulumi.export("aurora_endpoint", cluster.endpoint)
pulumi.export("connector_security_group_id", connector_sg.id)
pulumi.export("vpc_connector_arn", vpc_connector.arn)
pulumi.export("service_url", service.service_url)
