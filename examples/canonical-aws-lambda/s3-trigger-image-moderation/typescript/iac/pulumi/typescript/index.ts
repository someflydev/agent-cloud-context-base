import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const stack = pulumi.getStack();
const cfg = new pulumi.Config("accb");
const environment = cfg.get("environment") || stack;
const prefix = `accb-${environment}-s3mod`;
const secretPath = cfg.require("secretPath");
const s3modSecret = aws.secretsmanager.getSecret({ name: secretPath });

const images = new aws.s3.Bucket(`${prefix}-images-${stack}`, { bucket: `${prefix}-images-${stack}` });
const records = new aws.dynamodb.Table(`${prefix}-records-${stack}`, {
  name: `${prefix}-records-${stack}`,
  billingMode: "PAY_PER_REQUEST",
  hashKey: "pk",
  attributes: [{ name: "pk", type: "S" }]
});
const bus = new aws.cloudwatch.EventBus(`${prefix}-events-${stack}`, { name: `${prefix}-events-${stack}` });
const role = new aws.iam.Role(`${prefix}-lambda-${stack}`, {
  assumeRolePolicy: JSON.stringify({ Version: "2012-10-17", Statement: [{ Effect: "Allow", Principal: { Service: "lambda.amazonaws.com" }, Action: "sts:AssumeRole" }] })
});
new aws.iam.RolePolicyAttachment(`${prefix}-lambda-logs-${stack}`, { role: role.name, policyArn: "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" });
new aws.iam.RolePolicy(`${prefix}-lambda-access-${stack}`, {
  role: role.id,
  policy: pulumi.all([records.arn, bus.arn]).apply(([tableArn, busArn]) => JSON.stringify({
    Version: "2012-10-17",
    Statement: [
      { Effect: "Allow", Action: ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource: tableArn },
      { Effect: "Allow", Action: ["rekognition:DetectLabels", "rekognition:DetectModerationLabels"], Resource: "*" },
      { Effect: "Allow", Action: ["events:PutEvents"], Resource: busArn }
    ]
  }))
});
const fn = new aws.lambda.Function(`${prefix}-handler-${stack}`, {
  functionName: `${prefix}-handler-${stack}`,
  role: role.arn,
  runtime: "nodejs20.x",
  handler: "handler.handler",
  code: new pulumi.asset.AssetArchive({ "handler.js": new pulumi.asset.FileAsset("../../../src/handler.js") }),
  timeout: 30,
  environment: { variables: { TABLE_NAME: records.name, EVENT_BUS_NAME: bus.name, ENV_VAR_PREFIX: cfg.require("envVarPrefix"), SECRET_PATH: secretPath } }
});
const permission = new aws.lambda.Permission(`${prefix}-allow-s3-${stack}`, { action: "lambda:InvokeFunction", function: fn.name, principal: "s3.amazonaws.com", sourceArn: images.arn });
new aws.s3.BucketNotification(`${prefix}-images-notification-${stack}`, {
  bucket: images.id,
  lambdaFunctions: [{ lambdaFunctionArn: fn.arn, events: ["s3:ObjectCreated:*"] }]
}, { dependsOn: [permission] });

export const bucketName = images.bucket;
export const tableName = records.name;
export const eventBusName = bus.name;
export const functionName = fn.name;
export const secretArn = s3modSecret.then(secret => secret.arn);
