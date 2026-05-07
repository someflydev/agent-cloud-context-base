import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const stack = pulumi.getStack();
const cfg = new pulumi.Config("accb");
const environment = cfg.get("environment") || stack;
const prefix = `accb-${environment}-cdc`;
const secretPath = cfg.require("secretPath");
const cdcSecret = aws.secretsmanager.getSecret({ name: secretPath });

const changes = new aws.dynamodb.Table(`${prefix}-changes-${stack}`, { name: `${prefix}-changes-${stack}`, billingMode: "PAY_PER_REQUEST", hashKey: "pk", attributes: [{ name: "pk", type: "S" }] });
const sourceBus = new aws.cloudwatch.EventBus(`${prefix}-source-${stack}`, { name: `${prefix}-source-${stack}` });
const relayBus = new aws.cloudwatch.EventBus(`${prefix}-relay-${stack}`, { name: `${prefix}-relay-${stack}` });
const role = new aws.iam.Role(`${prefix}-lambda-${stack}`, { assumeRolePolicy: JSON.stringify({ Version: "2012-10-17", Statement: [{ Effect: "Allow", Principal: { Service: "lambda.amazonaws.com" }, Action: "sts:AssumeRole" }] }) });
new aws.iam.RolePolicyAttachment(`${prefix}-lambda-logs-${stack}`, { role: role.name, policyArn: "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" });
new aws.iam.RolePolicy(`${prefix}-lambda-access-${stack}`, { role: role.id, policy: pulumi.all([changes.arn, relayBus.arn]).apply(([tableArn, busArn]) => JSON.stringify({ Version: "2012-10-17", Statement: [{ Effect: "Allow", Action: ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource: tableArn }, { Effect: "Allow", Action: ["events:PutEvents"], Resource: busArn }] })) });
const fn = new aws.lambda.Function(`${prefix}-handler-${stack}`, { functionName: `${prefix}-handler-${stack}`, role: role.arn, runtime: "nodejs20.x", handler: "handler.handler", code: new pulumi.asset.AssetArchive({ "handler.js": new pulumi.asset.FileAsset("../../../src/handler.js") }), timeout: 15, environment: { variables: { TABLE_NAME: changes.name, RELAY_BUS_NAME: relayBus.name, ENV_VAR_PREFIX: cfg.require("envVarPrefix"), SECRET_PATH: secretPath } } });
const rule = new aws.cloudwatch.EventRule(`${prefix}-cdc-${stack}`, { name: `${prefix}-cdc-${stack}`, eventBusName: sourceBus.name, eventPattern: JSON.stringify({ source: ["accb.database"] }) });
new aws.cloudwatch.EventTarget(`${prefix}-lambda-${stack}`, { rule: rule.name, eventBusName: sourceBus.name, arn: fn.arn });
new aws.lambda.Permission(`${prefix}-allow-eventbridge-${stack}`, { action: "lambda:InvokeFunction", function: fn.name, principal: "events.amazonaws.com", sourceArn: rule.arn });

export const tableName = changes.name;
export const sourceBusName = sourceBus.name;
export const relayBusName = relayBus.name;
export const functionName = fn.name;
export const secretArn = cdcSecret.then(secret => secret.arn);
