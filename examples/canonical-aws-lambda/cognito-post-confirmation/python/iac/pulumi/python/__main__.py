import pulumi
import pulumi_aws as aws

stack = pulumi.get_stack()
config = pulumi.Config("accb")
environment = config.get("environment") or stack
prefix = f"accb-{environment}-cognito"
secret_path = config.require("secretPath")
cognito_secret = aws.secretsmanager.get_secret(name=secret_path)
profiles = aws.dynamodb.Table(f"{prefix}-profiles-{stack}", name=f"{prefix}-profiles-{stack}", billing_mode="PAY_PER_REQUEST", hash_key="pk", attributes=[aws.dynamodb.TableAttributeArgs(name="pk", type="S")])
bus = aws.cloudwatch.EventBus(f"{prefix}-signup-{stack}", name=f"{prefix}-signup-{stack}")
role = aws.iam.Role(f"{prefix}-lambda-{stack}", assume_role_policy='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}')
aws.iam.RolePolicyAttachment(f"{prefix}-lambda-logs-{stack}", role=role.name, policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
aws.iam.RolePolicy(f"{prefix}-lambda-access-{stack}", role=role.id, policy=pulumi.Output.all(profiles.arn, bus.arn).apply(lambda args: f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Action":["dynamodb:PutItem","dynamodb:UpdateItem"],"Resource":"{args[0]}"}},{{"Effect":"Allow","Action":["events:PutEvents"],"Resource":"{args[1]}"}}]}}'))
fn = aws.lambda_.Function(f"{prefix}-handler-{stack}", name=f"{prefix}-handler-{stack}", role=role.arn, runtime="python3.12", handler="handler.lambda_handler", code=pulumi.AssetArchive({"handler.py": pulumi.FileAsset("../../../src/handler.py")}), timeout=15, environment=aws.lambda_.FunctionEnvironmentArgs(variables={"TABLE_NAME": profiles.name, "EVENT_BUS_NAME": bus.name, "ENV_VAR_PREFIX": config.require("envVarPrefix"), "SECRET_PATH": secret_path}))
users = aws.cognito.UserPool(f"{prefix}-users-{stack}", name=f"{prefix}-users-{stack}", lambda_config=aws.cognito.UserPoolLambdaConfigArgs(post_confirmation=fn.arn))
aws.lambda_.Permission(f"{prefix}-allow-cognito-{stack}", action="lambda:InvokeFunction", function=fn.name, principal="cognito-idp.amazonaws.com", source_arn=users.arn)

pulumi.export("user_pool_id", users.id)
pulumi.export("table_name", profiles.name)
pulumi.export("event_bus_name", bus.name)
pulumi.export("function_name", fn.name)
pulumi.export("secret_arn", cognito_secret.arn)
