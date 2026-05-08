import pulumi
from pulumi_gcp import cloudrunv2, cloudscheduler, secretmanager, serviceaccount, storage


config = pulumi.Config("accb")
environment = config.require("environment")
name_prefix = f"accb-{environment}-cloudrun-nightly-report"
labels = {"managed_by": "accb", "environment": environment, "family": "canonical-cloud-run"}
image = config.get("image") or f"gcr.io/example/{name_prefix}:latest"
region = config.get("region") or "us-central1"
project = pulumi.Config("gcp").require("project")

job_sa = serviceaccount.Account(
    "job",
    account_id=f"{name_prefix}-job",
    display_name=f"accb {environment} Cloud Run nightly report job",
)

reports = storage.Bucket(
    "reports",
    name=f"{name_prefix}-reports",
    location="US",
    uniform_bucket_level_access=True,
    labels=labels,
)

reporting_secret = secretmanager.Secret(
    "reporting",
    secret_id=f"{name_prefix}-reporting",
    replication=secretmanager.SecretReplicationArgs(
        auto=secretmanager.SecretReplicationAutoArgs(),
    ),
    labels=labels,
)

nightly_report = cloudrunv2.Job(
    "nightly-report",
    name=f"{name_prefix}-job",
    location=region,
    template=cloudrunv2.JobTemplateArgs(
        template=cloudrunv2.JobTemplateTemplateArgs(
            service_account=job_sa.email,
            containers=[
                cloudrunv2.JobTemplateTemplateContainerArgs(
                    image=image,
                    args=["/cleanup"],
                    envs=[
                        cloudrunv2.JobTemplateTemplateContainerEnvArgs(name="REPORT_BUCKET", value=reports.name),
                        cloudrunv2.JobTemplateTemplateContainerEnvArgs(name="REPORTING_SECRET", value=reporting_secret.secret_id),
                    ],
                )
            ],
            max_retries=1,
            timeout="900s",
        )
    ),
    labels=labels,
)

schedule = cloudscheduler.Job(
    "nightly",
    name=f"{name_prefix}-schedule",
    region=region,
    schedule="0 6 * * *",
    time_zone="Etc/UTC",
    http_target=cloudscheduler.JobHttpTargetArgs(
        http_method="POST",
        uri=pulumi.Output.concat(
            "https://",
            region,
            "-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/",
            project,
            "/jobs/",
            nightly_report.name,
            ":run",
        ),
        oauth_token=cloudscheduler.JobHttpTargetOauthTokenArgs(service_account_email=job_sa.email),
    ),
)

pulumi.export("job_name", nightly_report.name)
pulumi.export("schedule_name", schedule.name)
pulumi.export("report_bucket", reports.name)
pulumi.export("reporting_secret", reporting_secret.secret_id)
