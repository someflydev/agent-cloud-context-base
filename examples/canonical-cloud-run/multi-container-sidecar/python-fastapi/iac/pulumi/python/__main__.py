import pulumi
from pulumi_gcp import cloudrunv2, serviceaccount


config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-cloudrun-sidecar"
labels = {"managed_by": "accb", "environment": environment, "family": "canonical-cloud-run"}
image = config.get("image") or f"gcr.io/example/{name_prefix}:latest"
region = config.get("region") or "us-central1"

service_sa = serviceaccount.Account(
    "service",
    account_id=f"{name_prefix}-svc",
    display_name=f"accb {environment} Cloud Run sidecar",
)

service = cloudrunv2.Service(
    "service",
    name=f"{name_prefix}-svc",
    location=region,
    template=cloudrunv2.ServiceTemplateArgs(
        service_account=service_sa.email,
        containers=[
            cloudrunv2.ServiceTemplateContainerArgs(
                name="app",
                image=image,
                ports=[cloudrunv2.ServiceTemplateContainerPortArgs(container_port=8080)],
                envs=[
                    cloudrunv2.ServiceTemplateContainerEnvArgs(
                        name="OTEL_EXPORTER_OTLP_ENDPOINT",
                        value="http://127.0.0.1:4318",
                    )
                ],
                resources=cloudrunv2.ServiceTemplateContainerResourcesArgs(
                    limits={"cpu": "1000m", "memory": "512Mi"}
                ),
            ),
            cloudrunv2.ServiceTemplateContainerArgs(
                name="otel",
                image="otel/opentelemetry-collector@sha256:0000000000000000000000000000000000000000000000000000000000000000",
                args=["--config=/etc/otelcol/config.yaml"],
                resources=cloudrunv2.ServiceTemplateContainerResourcesArgs(
                    limits={"cpu": "250m", "memory": "256Mi"}
                ),
            ),
        ],
    ),
    labels=labels,
)

pulumi.export("service_account_email", service_sa.email)
pulumi.export("service_uri", service.uri)
pulumi.export("otel_endpoint", "http://127.0.0.1:4318")
