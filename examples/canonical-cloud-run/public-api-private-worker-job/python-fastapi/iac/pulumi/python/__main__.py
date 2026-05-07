import pulumi
from pulumi_gcp import cloudrunv2, firestore, projects, pubsub, secretmanager, serviceaccount, storage


config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-cloudrun-public-worker"
labels = {"managed_by": "accb", "environment": environment, "family": "canonical-cloud-run"}
image = config.get("image") or f"gcr.io/example/{name_prefix}:latest"
region = config.get("region") or "us-central1"

service_sa = serviceaccount.Account(
    "service",
    account_id=f"{name_prefix}-svc",
    display_name=f"accb {environment} Cloud Run public worker",
)

attachments = storage.Bucket(
    "attachments",
    name=f"{name_prefix}-attachments",
    location="US",
    uniform_bucket_level_access=True,
    labels=labels,
)

review_topic = pubsub.Topic("review", name=f"{name_prefix}-review", labels=labels)

workflow_db = firestore.Database(
    "workflow",
    name=f"{name_prefix}-workflow",
    location_id=region,
    type="FIRESTORE_NATIVE",
)

reviewer_secret = secretmanager.Secret(
    "reviewer",
    secret_id=f"{name_prefix}-reviewer",
    replication=secretmanager.SecretReplicationArgs(
        auto=secretmanager.SecretReplicationAutoArgs(),
    ),
    labels=labels,
)

public_service = cloudrunv2.Service(
    "public",
    name=f"{name_prefix}-public",
    location=region,
    template=cloudrunv2.ServiceTemplateArgs(
        service_account=service_sa.email,
        containers=[
            cloudrunv2.ServiceTemplateContainerArgs(
                image=image,
                envs=[
                    cloudrunv2.ServiceTemplateContainerEnvArgs(name="ATTACHMENT_BUCKET", value=attachments.name),
                    cloudrunv2.ServiceTemplateContainerEnvArgs(name="REVIEW_TOPIC", value=review_topic.name),
                ],
            )
        ],
    ),
    labels=labels,
)

private_worker = cloudrunv2.Service(
    "private-worker",
    name=f"{name_prefix}-private-worker",
    location=region,
    ingress="INGRESS_TRAFFIC_INTERNAL_ONLY",
    template=cloudrunv2.ServiceTemplateArgs(
        service_account=service_sa.email,
        containers=[
            cloudrunv2.ServiceTemplateContainerArgs(
                image=image,
                envs=[
                    cloudrunv2.ServiceTemplateContainerEnvArgs(name="REVIEWER_SECRET", value=reviewer_secret.secret_id),
                    cloudrunv2.ServiceTemplateContainerEnvArgs(name="CALLBACK_AUDIENCE", value=f"{name_prefix}-private-worker"),
                ],
            )
        ],
    ),
    labels=labels,
)

cleanup_job = cloudrunv2.Job(
    "nightly-cleanup",
    name=f"{name_prefix}-cleanup",
    location=region,
    template=cloudrunv2.JobTemplateArgs(
        template=cloudrunv2.JobTemplateTemplateArgs(
            service_account=service_sa.email,
            containers=[cloudrunv2.JobTemplateTemplateContainerArgs(image=image, args=["/cleanup"])],
            max_retries=1,
        )
    ),
    labels=labels,
)

projects.IAMMember(
    "worker-invoker",
    project=pulumi.Config("gcp").require("project"),
    role="roles/run.invoker",
    member=service_sa.email.apply(lambda email: f"serviceAccount:{email}"),
)

pulumi.export("service_account_email", service_sa.email)
pulumi.export("attachment_bucket", attachments.name)
pulumi.export("review_topic", review_topic.name)
pulumi.export("public_service_uri", public_service.uri)
pulumi.export("private_worker_uri", private_worker.uri)
pulumi.export("cleanup_job_name", cleanup_job.name)
pulumi.export("workflow_database", workflow_db.name)
pulumi.export("reviewer_secret", reviewer_secret.secret_id)
