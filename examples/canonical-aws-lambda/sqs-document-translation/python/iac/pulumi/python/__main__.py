import pulumi
import pulumi_aws as aws

stack = pulumi.get_stack()
config = pulumi.Config("accb")
environment = config.get("environment") or stack
prefix = f"accb-{environment}-translate"
secret_path = config.require("secretPath")
translate_secret = aws.secretsmanager.get_secret(name=secret_path)
source = aws.s3.Bucket(f"{prefix}-source-{stack}", bucket=f"{prefix}-source-{stack}")
dest = aws.s3.Bucket(f"{prefix}-dest-{stack}", bucket=f"{prefix}-dest-{stack}")
dlq = aws.sqs.Queue(f"{prefix}-dlq-{stack}", name=f"{prefix}-dlq-{stack}")
jobs = aws.sqs.Queue(f"{prefix}-jobs-{stack}", name=f"{prefix}-jobs-{stack}", visibility_timeout_seconds=120, redrive_policy=dlq.arn.apply(lambda arn: f'{{"deadLetterTargetArn":"{arn}","maxReceiveCount":3}}'))
table = aws.dynamodb.Table(f"{prefix}-jobs-{stack}", name=f"{prefix}-jobs-{stack}", billing_mode="PAY_PER_REQUEST", hash_key="pk", attributes=[aws.dynamodb.TableAttributeArgs(name="pk", type="S")])
role = aws.iam.Role(f"{prefix}-lambda-{stack}", assume_role_policy='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}')
aws.iam.RolePolicyAttachment(f"{prefix}-lambda-logs-{stack}", role=role.name, policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
aws.iam.RolePolicy(f"{prefix}-lambda-access-{stack}", role=role.id, policy=pulumi.Output.all(source.arn, dest.arn, table.arn, jobs.arn).apply(lambda args: f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Action":["s3:GetObject"],"Resource":"{args[0]}/*"}},{{"Effect":"Allow","Action":["s3:PutObject"],"Resource":"{args[1]}/*"}},{{"Effect":"Allow","Action":["dynamodb:PutItem","dynamodb:UpdateItem"],"Resource":"{args[2]}"}},{{"Effect":"Allow","Action":["translate:TranslateText"],"Resource":"*"}},{{"Effect":"Allow","Action":["sqs:ReceiveMessage","sqs:DeleteMessage","sqs:GetQueueAttributes"],"Resource":"{args[3]}"}}]}}'))
fn = aws.lambda_.Function(f"{prefix}-handler-{stack}", name=f"{prefix}-handler-{stack}", role=role.arn, runtime="python3.12", handler="handler.lambda_handler", code=pulumi.AssetArchive({"handler.py": pulumi.FileAsset("../../../src/handler.py")}), timeout=60, environment=aws.lambda_.FunctionEnvironmentArgs(variables={"TABLE_NAME": table.name, "SOURCE_BUCKET": source.bucket, "DEST_BUCKET": dest.bucket, "ENV_VAR_PREFIX": config.require("envVarPrefix"), "SECRET_PATH": secret_path}))
aws.lambda_.EventSourceMapping(f"{prefix}-jobs-{stack}", event_source_arn=jobs.arn, function_name=fn.arn, batch_size=1)

pulumi.export("source_bucket", source.bucket)
pulumi.export("dest_bucket", dest.bucket)
pulumi.export("queue_url", jobs.url)
pulumi.export("table_name", table.name)
pulumi.export("function_name", fn.name)
pulumi.export("secret_arn", translate_secret.arn)
