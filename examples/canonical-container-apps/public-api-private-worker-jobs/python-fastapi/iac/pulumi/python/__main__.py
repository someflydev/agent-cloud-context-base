import pulumi
from pulumi_azure_native import app, containerregistry, documentdb, keyvault, managedidentity, operationalinsights, resources, servicebus, storage


config = pulumi.Config("accb")
environment = config.require("environment")
location = config.get("location") or "eastus"
image = config.get("image") or f"accb{environment}acr.azurecr.io/aca-public-worker:latest"
name_prefix = f"accb-{environment}-aca-public-worker"
tags = {"ManagedBy": "accb", "Environment": environment, "Family": "canonical-container-apps"}

resource_group = resources.ResourceGroup("main", resource_group_name=f"{name_prefix}-rg", location=location, tags=tags)

identity = managedidentity.UserAssignedIdentity(
    "aca",
    resource_group_name=resource_group.name,
    resource_name_=f"{name_prefix}-mi",
    location=resource_group.location,
    tags=tags,
)

logs = operationalinsights.Workspace(
    "logs",
    resource_group_name=resource_group.name,
    workspace_name=f"{name_prefix}-logs",
    location=resource_group.location,
    sku=operationalinsights.WorkspaceSkuArgs(name="PerGB2018"),
    retention_in_days=30,
    tags=tags,
)

environment_resource = app.ManagedEnvironment(
    "env",
    resource_group_name=resource_group.name,
    environment_name=f"{name_prefix}-env",
    location=resource_group.location,
    app_logs_configuration=app.AppLogsConfigurationArgs(
        destination="log-analytics",
        log_analytics_configuration=app.LogAnalyticsConfigurationArgs(
            customer_id=logs.customer_id,
            shared_key=logs.shared_keys.apply(lambda keys: keys.primary_shared_key),
        ),
    ),
    tags=tags,
)

acr = containerregistry.Registry(
    "acr",
    registry_name=f"accb{environment}acapublicworkeracr",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=containerregistry.SkuArgs(name="Basic"),
    admin_user_enabled=False,
    tags=tags,
)

bus = servicebus.Namespace(
    "events",
    namespace_name=f"{name_prefix}-sb",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=servicebus.SBSkuArgs(name="Standard", tier="Standard"),
    tags=tags,
)

queue = servicebus.Queue(
    "work",
    queue_name=f"{name_prefix}-work",
    namespace_name=bus.name,
    resource_group_name=resource_group.name,
)

cosmos = documentdb.DatabaseAccount(
    "state",
    account_name=f"{name_prefix}-cosmos",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    database_account_offer_type="Standard",
    locations=[documentdb.LocationArgs(location_name=resource_group.location, failover_priority=0)],
    consistency_policy=documentdb.ConsistencyPolicyArgs(default_consistency_level="Session"),
    tags=tags,
)

attachments = storage.StorageAccount(
    "attachments",
    account_name=f"accb{environment}acapublicblob",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=storage.SkuArgs(name="Standard_LRS"),
    kind="StorageV2",
    tags=tags,
)

vault = keyvault.Vault(
    "secrets",
    vault_name=f"{name_prefix}-kv",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    properties=keyvault.VaultPropertiesArgs(
        tenant_id=identity.tenant_id,
        sku=keyvault.SkuArgs(family="A", name="standard"),
    ),
    tags=tags,
)

public_api = app.ContainerApp(
    "public-api",
    container_app_name=f"{name_prefix}-api",
    resource_group_name=resource_group.name,
    managed_environment_id=environment_resource.id,
    location=resource_group.location,
    configuration=app.ConfigurationArgs(
        ingress=app.IngressArgs(external=True, target_port=8080),
        secrets=[app.SecretArgs(name="api-key", key_vault_url=vault.properties.vault_uri.apply(lambda uri: f"{uri}secrets/api-key"), identity=identity.id)],
    ),
    identity=app.ManagedServiceIdentityArgs(type="UserAssigned", user_assigned_identities={identity.id: {}}),
    template=app.TemplateArgs(
        containers=[
            app.ContainerArgs(
                name="api",
                image=image,
                env=[
                    app.EnvironmentVarArgs(name="SERVICEBUS_QUEUE", value=queue.name),
                    app.EnvironmentVarArgs(name="API_SECRET_NAME", secret_ref="api-key"),
                ],
                resources=app.ContainerResourcesArgs(cpu=0.5, memory="1Gi"),
            )
        ],
        scale=app.ScaleArgs(min_replicas=1, max_replicas=5),
    ),
    tags=tags,
)

private_worker = app.ContainerApp(
    "private-worker",
    container_app_name=f"{name_prefix}-worker",
    resource_group_name=resource_group.name,
    managed_environment_id=environment_resource.id,
    location=resource_group.location,
    configuration=app.ConfigurationArgs(ingress=app.IngressArgs(external=False, target_port=8080)),
    identity=app.ManagedServiceIdentityArgs(type="UserAssigned", user_assigned_identities={identity.id: {}}),
    template=app.TemplateArgs(
        containers=[app.ContainerArgs(name="worker", image=image, resources=app.ContainerResourcesArgs(cpu=0.5, memory="1Gi"))],
        scale=app.ScaleArgs(
            min_replicas=0,
            max_replicas=10,
            rules=[app.ScaleRuleArgs(name="servicebus-depth", custom=app.CustomScaleRuleArgs(type="azure-servicebus", metadata={"queueName": queue.name, "messageCount": "5"}))],
        ),
    ),
    tags=tags,
)

retry_job = app.Job(
    "retry-job",
    job_name=f"{name_prefix}-retry",
    resource_group_name=resource_group.name,
    managed_environment_id=environment_resource.id,
    location=resource_group.location,
    configuration=app.JobConfigurationArgs(
        trigger_type="Event",
        event_trigger_config=app.JobConfigurationEventTriggerConfigArgs(
            parallelism=1,
            replica_completion_count=1,
            scale=app.JobScaleArgs(min_executions=0, max_executions=5, rules=[app.JobScaleRuleArgs(name="servicebus-retry", type="azure-servicebus", metadata={"queueName": queue.name, "messageCount": "5"})]),
        ),
        replica_timeout=300,
        replica_retry_limit=1,
    ),
    template=app.JobTemplateArgs(containers=[app.ContainerArgs(name="retry", image=image, args=["/retry"], resources=app.ContainerResourcesArgs(cpu=0.5, memory="1Gi"))]),
    tags=tags,
)

pulumi.export("public_api_url", public_api.configuration.apply(lambda cfg: cfg.ingress.fqdn if cfg and cfg.ingress else None))
pulumi.export("private_worker_name", private_worker.name)
pulumi.export("retry_job_name", retry_job.name)
pulumi.export("servicebus_queue", queue.name)
pulumi.export("cosmos_account", cosmos.name)
pulumi.export("attachment_account", attachments.name)
pulumi.export("key_vault_uri", vault.properties.vault_uri)
pulumi.export("managed_identity_id", identity.id)
pulumi.export("acr_login_server", acr.login_server)
