import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const stack = pulumi.getStack();
const cfg = new pulumi.Config("accb");
const environment = cfg.get("environment") || stack;
const prefix = `accb-${environment}-stripe`;
const secretPath = cfg.require("secretPath");

const stripeSecret = aws.secretsmanager.getSecret({ name: secretPath });
const events = new aws.dynamodb.Table(`${prefix}-events-${stack}`, {
  name: `${prefix}-events-${stack}`,
  billingMode: "PAY_PER_REQUEST",
  hashKey: "pk",
  attributes: [{ name: "pk", type: "S" }]
});
const api = new aws.apigatewayv2.Api(`${prefix}-api-${stack}`, {
  name: `${prefix}-api-${stack}`,
  protocolType: "HTTP"
});
const role = new aws.iam.Role(`${prefix}-workflow-${stack}`, {
  assumeRolePolicy: JSON.stringify({ Version: "2012-10-17", Statement: [{ Effect: "Allow", Principal: { Service: "states.amazonaws.com" }, Action: "sts:AssumeRole" }] })
});
const workflow = new aws.sfn.StateMachine(`${prefix}-workflow-${stack}`, {
  name: `${prefix}-workflow-${stack}`,
  roleArn: role.arn,
  definition: JSON.stringify({ StartAt: "Accepted", States: { Accepted: { Type: "Succeed" } } })
});
const lambdaRole = new aws.iam.Role(`${prefix}-lambda-${stack}`, {
  assumeRolePolicy: JSON.stringify({ Version: "2012-10-17", Statement: [{ Effect: "Allow", Principal: { Service: "lambda.amazonaws.com" }, Action: "sts:AssumeRole" }] })
});
new aws.iam.RolePolicyAttachment(`${prefix}-lambda-logs-${stack}`, {
  role: lambdaRole.name,
  policyArn: "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
});
new aws.iam.RolePolicy(`${prefix}-lambda-access-${stack}`, {
  role: lambdaRole.id,
  policy: pulumi.all([events.arn, workflow.arn]).apply(([tableArn, workflowArn]) => JSON.stringify({
    Version: "2012-10-17",
    Statement: [
      { Effect: "Allow", Action: ["dynamodb:PutItem"], Resource: tableArn },
      { Effect: "Allow", Action: ["states:StartExecution"], Resource: workflowArn },
      { Effect: "Allow", Action: ["secretsmanager:GetSecretValue"], Resource: "*" }
    ]
  }))
});
const handler = new aws.lambda.Function(`${prefix}-handler-${stack}`, {
  functionName: `${prefix}-handler-${stack}`,
  role: lambdaRole.arn,
  runtime: "nodejs20.x",
  handler: "handler.handler",
  code: new pulumi.asset.AssetArchive({ "handler.js": new pulumi.asset.FileAsset("../../../src/handler.js") }),
  timeout: 15,
  environment: {
    variables: {
      TABLE_NAME: events.name,
      WORKFLOW_ARN: workflow.arn,
      STRIPE_SECRET: secretPath,
      ENV_VAR_PREFIX: cfg.require("envVarPrefix")
    }
  }
});
const integration = new aws.apigatewayv2.Integration(`${prefix}-lambda-${stack}`, {
  apiId: api.id,
  integrationType: "AWS_PROXY",
  integrationUri: handler.invokeArn,
  payloadFormatVersion: "2.0"
});
new aws.apigatewayv2.Route(`${prefix}-webhook-${stack}`, {
  apiId: api.id,
  routeKey: "POST /stripe/webhook",
  target: pulumi.interpolate`integrations/${integration.id}`
});
new aws.lambda.Permission(`${prefix}-allow-apigw-${stack}`, {
  action: "lambda:InvokeFunction",
  function: handler.name,
  principal: "apigateway.amazonaws.com",
  sourceArn: pulumi.interpolate`${api.executionArn}/*/*`
});

export const tableName = events.name;
export const apiEndpoint = api.apiEndpoint;
export const workflowArn = workflow.arn;
export const functionName = handler.name;
export const secretArn = stripeSecret.then((secret) => secret.arn);
