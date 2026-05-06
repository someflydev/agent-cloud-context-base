import pulumi
import pulumi_aws as aws

stack = pulumi.get_stack()
config = pulumi.Config("accb")
environment = config.get("environment") or stack
prefix = f"accb-{environment}-s3mod"
secret_path = config.require("secretPath")

rekognition_secret = aws.secretsmanager.get_secret(name=secret_path)
images = aws.s3.Bucket(f"{prefix}-images-{stack}", bucket=f"{prefix}-images-{stack}")
records = aws.dynamodb.Table(
    f"{prefix}-records-{stack}",
    name=f"{prefix}-records-{stack}",
    billing_mode="PAY_PER_REQUEST",
    hash_key="pk",
    attributes=[aws.dynamodb.TableAttributeArgs(name="pk", type="S")],
)
events = aws.cloudwatch.EventBus(f"{prefix}-events-{stack}", name=f"{prefix}-events-{stack}")
role = aws.iam.Role(
    f"{prefix}-lambda-{stack}",
    assume_role_policy='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}',
)
aws.iam.RolePolicyAttachment(
    f"{prefix}-lambda-logs-{stack}",
    role=role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
)
aws.iam.RolePolicy(
    f"{prefix}-lambda-access-{stack}",
    role=role.id,
    policy=pulumi.Output.all(records.arn, events.arn).apply(
        lambda args: f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Action":["dynamodb:PutItem","dynamodb:UpdateItem"],"Resource":"{args[0]}"}},{{"Effect":"Allow","Action":["rekognition:DetectLabels","rekognition:DetectModerationLabels"],"Resource":"*"}},{{"Effect":"Allow","Action":["events:PutEvents"],"Resource":"{args[1]}"}}]}}'
    ),
)
function = aws.lambda_.Function(
    f"{prefix}-handler-{stack}",
    name=f"{prefix}-handler-{stack}",
    role=role.arn,
    runtime="python3.12",
    handler="handler.lambda_handler",
    code=pulumi.AssetArchive({"handler.py": pulumi.FileAsset("../../../src/handler.py")}),
    timeout=30,
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "TABLE_NAME": records.name,
            "EVENT_BUS_NAME": events.name,
            "ENV_VAR_PREFIX": config.require("envVarPrefix"),
            "SECRET_PATH": secret_path,
        }
    ),
)
permission = aws.lambda_.Permission(
    f"{prefix}-allow-s3-{stack}",
    action="lambda:InvokeFunction",
    function=function.name,
    principal="s3.amazonaws.com",
    source_arn=images.arn,
)
aws.s3.BucketNotification(
    f"{prefix}-images-notification-{stack}",
    bucket=images.id,
    lambda_functions=[
        aws.s3.BucketNotificationLambdaFunctionArgs(
            lambda_function_arn=function.arn,
            events=["s3:ObjectCreated:*"],
        )
    ],
    opts=pulumi.ResourceOptions(depends_on=[permission]),
)

pulumi.export("bucket_name", images.bucket)
pulumi.export("table_name", records.name)
pulumi.export("event_bus_name", events.name)
pulumi.export("role_name", role.name)
pulumi.export("function_name", function.name)
pulumi.export("secret_arn", rekognition_secret.arn)
