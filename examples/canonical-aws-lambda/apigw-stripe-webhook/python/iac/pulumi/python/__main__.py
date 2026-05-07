import pulumi
import pulumi_aws as aws

stack = pulumi.get_stack()
config = pulumi.Config("accb")
environment = config.get("environment") or stack
prefix = f"accb-{environment}-stripe"
secret_path = config.require("secretPath")
stripe_secret = aws.secretsmanager.get_secret(name=secret_path)

events = aws.dynamodb.Table(f"{prefix}-events-{stack}", name=f"{prefix}-events-{stack}", billing_mode="PAY_PER_REQUEST", hash_key="pk", attributes=[aws.dynamodb.TableAttributeArgs(name="pk", type="S")])
workflow_role = aws.iam.Role(f"{prefix}-workflow-{stack}", assume_role_policy='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"states.amazonaws.com"},"Action":"sts:AssumeRole"}]}')
workflow = aws.sfn.StateMachine(f"{prefix}-workflow-{stack}", name=f"{prefix}-workflow-{stack}", role_arn=workflow_role.arn, definition='{"StartAt":"Accepted","States":{"Accepted":{"Type":"Succeed"}}}')
api = aws.apigatewayv2.Api(f"{prefix}-api-{stack}", name=f"{prefix}-api-{stack}", protocol_type="HTTP")
role = aws.iam.Role(f"{prefix}-lambda-{stack}", assume_role_policy='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}')
aws.iam.RolePolicyAttachment(f"{prefix}-lambda-logs-{stack}", role=role.name, policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
aws.iam.RolePolicy(f"{prefix}-lambda-access-{stack}", role=role.id, policy=pulumi.Output.all(events.arn, workflow.arn, stripe_secret.arn).apply(lambda args: f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Action":["dynamodb:PutItem"],"Resource":"{args[0]}"}},{{"Effect":"Allow","Action":["states:StartExecution"],"Resource":"{args[1]}"}},{{"Effect":"Allow","Action":["secretsmanager:GetSecretValue"],"Resource":"{args[2]}"}}]}}'))
fn = aws.lambda_.Function(f"{prefix}-handler-{stack}", name=f"{prefix}-handler-{stack}", role=role.arn, runtime="python3.12", handler="handler.lambda_handler", code=pulumi.AssetArchive({"handler.py": pulumi.FileAsset("../../../src/handler.py")}), timeout=15, environment=aws.lambda_.FunctionEnvironmentArgs(variables={"TABLE_NAME": events.name, "WORKFLOW_ARN": workflow.arn, "STRIPE_SECRET": secret_path, "ENV_VAR_PREFIX": config.require("envVarPrefix")}))
integration = aws.apigatewayv2.Integration(f"{prefix}-lambda-{stack}", api_id=api.id, integration_type="AWS_PROXY", integration_uri=fn.invoke_arn, payload_format_version="2.0")
aws.apigatewayv2.Route(f"{prefix}-webhook-{stack}", api_id=api.id, route_key="POST /stripe/webhook", target=pulumi.Output.concat("integrations/", integration.id))
aws.lambda_.Permission(f"{prefix}-allow-apigw-{stack}", action="lambda:InvokeFunction", function=fn.name, principal="apigateway.amazonaws.com", source_arn=pulumi.Output.concat(api.execution_arn, "/*/*"))

pulumi.export("table_name", events.name)
pulumi.export("api_endpoint", api.api_endpoint)
pulumi.export("workflow_arn", workflow.arn)
pulumi.export("function_name", fn.name)
pulumi.export("secret_arn", stripe_secret.arn)
